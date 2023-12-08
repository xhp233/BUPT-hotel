from django.utils import timezone
class Scheduler:
    def __init__(self, target_temperature=22.0, billing_rate=1.0, temperature_change_rate=0.5, max_running=3):
        self.coolheat = 1
        self.target_temperature = target_temperature
        self.billing_rate = billing_rate
        self.max_runningroom = max_running
        self.temperature_change_rate = temperature_change_rate
        self.rooms = {}
        self.running_rooms = []  # 记录当前正在运行的房间
        self.service_queue = []  # 记录服务队列，服务时长最长的房间
        self.waiting_queue = []  # 记录等待队列
        self.request_queue = []  # 记录请求队列

    def set_params(self, target_temperature, billing_rate, temperature_change_rate, coolheat):
        '''
        设置调度器参数
        :param target_temperature: 目标温度
        :param billing_rate: 费率
        :param temperature_change_rate: 温度变化率
        :param coolheat: 制冷制热(-1为制冷，1为制热)
        '''
        self.target_temperature = float(target_temperature)
        for room_number in self.rooms:
            self.rooms[room_number]['target_temperature'] = self.target_temperature
        self.billing_rate = float(billing_rate)
        self.temperature_change_rate = float(temperature_change_rate)
        self.coolheat = float(coolheat)

    def add_room(self, room_number, initial_temperature):
        '''
        添加房间
        :param room_number: 房间号
        :param initial_temperature: 初始温度
        '''
        self.rooms[room_number] = {
            'current_temperature': initial_temperature,
            'target_temperature': self.target_temperature,
            'running': True,#启动了空调调度程序
            'fan_speed': 'mid',
            'total_service_time': 0, #总服务时间
            'time_remaining':0,#服务队列里剩余时间
            'current_cost': 0,
            'request_time': timezone.now(),#请求时间
            # 'history': [],
        }

    def start_air_conditioning(self, room_number):
        '''
        开启空调
        :param room_number: 房间号
        '''
        print("room " + room_number + " start_air_conditioning")
        self.rooms[room_number]['step_cost'] = []
        self.request_queue.append(room_number)
        self.rooms[room_number]['request_time'] = timezone.now()
        self.rooms[room_number]['running']=True
        self.rooms[room_number]['fan_speed']='mid'
        self.rooms[room_number]['target_temperature']=self.target_temperature
        self.running_rooms.append(room_number)
        self.waiting_queue.append(room_number)

    def set_target_temperature(self, room_number, target_temperature):
        '''
        设置目标温度
        :param room_number: 房间号
        :param target_temperature: 目标温度
        '''
        print("room " + room_number + " set_target_temperature " + str(target_temperature))
        self.rooms[room_number]['step_cost'] = []
        self.request_queue.append(room_number)
        self.rooms[room_number]['request_time'] = timezone.now()
        self.rooms[room_number]['target_temperature'] = float(target_temperature)

    def set_fan_speed(self, room_number, fan_speed):
        '''
        设置风速
        :param room_number: 房间号
        :param fan_speed: 风速
        '''
        print("room " + room_number + " set_fan_speed " + fan_speed)
        self.rooms[room_number]['step_cost'] = []
        self.request_queue.append(room_number)
        self.rooms[room_number]['request_time'] = timezone.now()
        self.rooms[room_number]['fan_speed'] = fan_speed

    def stop_air_conditioning(self, room_number):
        '''
        关闭空调
        :param room_number: 房间号
        '''
        print("room " + room_number + " stop_air_conditioning")
        self.rooms[room_number]['step_cost'] = []
        self.request_queue.append(room_number)
        self.rooms[room_number]['request_time'] = timezone.now()
        if room_number in self.running_rooms:
            self.running_rooms.remove(room_number)
        if room_number in self.service_queue:
            self.service_queue.remove(room_number)
        if room_number in self.waiting_queue:
            self.waiting_queue.remove(room_number)

        self.rooms[room_number]['running'] = False

    def update_temperature(self, room_number):
        '''
        更新房间温度
        :param room_number: 房间号
        '''
        if self.rooms[room_number]['running']:
            # Determine temperature change rate based on fan speed
            fan_speed = self.rooms[room_number]['fan_speed']
            if fan_speed == 'high':
                temperature_change_rate = 1.0
            elif fan_speed == 'mid':
                temperature_change_rate = 1/2
            elif fan_speed == 'low':
                temperature_change_rate = 1/3
            else:
                # Handle unknown fan speed (optional)
                temperature_change_rate = 0.5

            # Update temperature
            self.rooms[room_number]['current_temperature'] += temperature_change_rate * self.coolheat
            self.rooms[room_number]['current_cost'] += self.billing_rate * temperature_change_rate

    def priority_scheduling(self):
        '''
        优先级调度算法
        '''
        # 按照房间风速大小和在等待队列的先后顺序排序
        remaining_rooms = [room for room in self.waiting_queue if float(self.rooms[room]['current_temperature']) < float(self.rooms[room]['target_temperature'])]
        sorted_rooms = sorted(
           remaining_rooms,
            key=lambda x: (self.rooms[x]['fan_speed'], self.waiting_queue.index(x))
        )
        # 将已经达到目标温度的房间添加到排序结果的末尾
        sorted_rooms += [room for room in self.waiting_queue if room not in remaining_rooms]

        if sorted_rooms:
            return sorted_rooms[0]

        return None

    def step(self):
        '''
        调度器每一步执行的操作
        '''
        # Step 1: 运行上一时刻服务队列里的房间，更新温度并减少服务时间
        for room_number in self.service_queue:
            if self.service_queue is not None:
                self.update_temperature(room_number)
                self.rooms[room_number]['time_remaining'] -= 1

        # Step 2: 如果服务队列中房间不足3个，使用优先级调度算法将房间加入服务队列

        if len(self.service_queue) < self.max_runningroom :#服务队列里小于三个房间
            if len(self.running_rooms) > self.max_runningroom :#总运行房间大于三个房间
                while len(self.service_queue) < self.max_runningroom:
                    room_to_add = self.priority_scheduling()
                    if room_to_add is not None:
                        self.waiting_queue.remove(room_to_add)
                        self.service_queue.append(room_to_add)
                        self.rooms[room_to_add]['time_remaining'] = 2
                        self.update_temperature(room_to_add)
                        self.rooms[room_to_add]['time_remaining'] -= 1
            else:#总运行房间小于等于三个房间
                while len(self.service_queue) < len(self.running_rooms):
                    room_to_add = self.priority_scheduling()
                    if room_to_add is not None:
                        self.waiting_queue.remove(room_to_add)
                        self.service_queue.append(room_to_add)
                        self.rooms[room_to_add]['time_remaining'] = 2
                        self.update_temperature(room_to_add)
                        self.rooms[room_to_add]['time_remaining'] -= 1
                    if room_to_add is None:
                        break
                    
        # Step 3: 处理房间更改请求，更新房间状态

        for room_number in list(self.service_queue):
            if (self.rooms[room_number]['target_temperature'] - self.rooms[room_number]['current_temperature'] <= 0.1 ):
                # 房间到达目标温度 退出服务队列
                self.rooms[room_number]['current_temperature'] = self.rooms[room_number][ 'target_temperature']
                self.service_queue.remove(room_number)
                self.waiting_queue.append(room_number)
        for room_number in list(self.rooms):
            # 如果房间关机，执行回温
            if not self.rooms[room_number]['running']:
                self.rooms[room_number]['current_temperature'] -= 0.5

        # Step 4: 更新进入等待队列的房间
        for room_number in list(self.service_queue):
            if self.rooms[room_number]['time_remaining'] <= 0:
                # 房间服务时间到，退出服务队列，进入等待队列
                self.service_queue.remove(room_number)
                self.waiting_queue.append(room_number)

scheduler = Scheduler()

if __name__ == '__main__':
    # 添加房间
    scheduler.add_room('room_one', 10)
    scheduler.add_room('room_two', 15)
    scheduler.add_room('room_three', 18)
    scheduler.add_room('room_four', 12)
    scheduler.add_room('room_five', 14)

    # 模拟运行时长
    for minute in range(1, 27): 
        #每个循环 先遍历数据库的请求
        if minute == 1:
            scheduler.start_air_conditioning('room_one')  # 房间一开机
        elif minute == 2:
            scheduler.set_target_temperature('room_one', 24)  # 房间一设置温度
            scheduler.start_air_conditioning('room_two')  # 房间二开机
        elif minute == 3:
            scheduler.start_air_conditioning('room_three')  # 房间三开机
        elif minute == 4:
            scheduler.set_target_temperature('room_two', 25)  # 房间二设置温度
            scheduler.start_air_conditioning('room_four')  # 房间四开机
            scheduler.start_air_conditioning('room_five')  # 房间五开机
        elif minute == 5:
            scheduler.set_target_temperature('room_three', 27)  # 房间三设置温度
            scheduler.set_fan_speed('room_five', 'high')  # 房间五设置风速
        elif minute == 6:
            scheduler.set_fan_speed('room_one', 'high')  # 房间一设置风速
        elif minute == 8:
            scheduler.set_target_temperature('room_five', 24)  # 房间五设置温度
        elif minute == 10:
            scheduler.set_target_temperature('room_one', 28)  # 房间一设置温度
            scheduler.set_fan_speed('room_four', 'high')  # 房间四设置风速
            scheduler.set_target_temperature('room_four', 28)  # 房间四设置温度
        elif minute == 12:
            scheduler.set_fan_speed('room_five', 'mid')  # 房间五设置风速
        elif minute==13:
            scheduler.set_fan_speed('room_two', 'high')  # 房间四二设置风速
        elif minute == 15:
            scheduler.stop_air_conditioning('room_one')  # 房间一关机
            scheduler.set_fan_speed('room_three', 'low')  # 房间三设置风速
        elif minute == 17:
            scheduler.stop_air_conditioning('room_five')  # 房间五关机
        elif minute==18:
            scheduler.set_fan_speed('room_three','high')
        elif minute == 19:
            scheduler.start_air_conditioning('room_one')  # 房间一开机
            scheduler.set_target_temperature('room_four', 25)  # 房间四设置温度
            scheduler.set_fan_speed('room_four', 'mid')  # 房间四设置风速
        elif minute == 21:
            scheduler.set_target_temperature('room_two', 27)  # 房间二设置温度
            scheduler.set_fan_speed('room_two', 'mid')  # 房间二设置风速
            scheduler.start_air_conditioning('room_five')  # 房间五开机
        elif minute == 25:
            scheduler.stop_air_conditioning('room_one')  # 房间一关机
            scheduler.stop_air_conditioning('room_three')  # 房间三关机
            scheduler.stop_air_conditioning('room_five')  # 房间五关机
        elif minute == 26:
            scheduler.stop_air_conditioning('room_two')  # 房间二关机
            scheduler.stop_air_conditioning('room_four')  # 房间四关机

        scheduler.step()