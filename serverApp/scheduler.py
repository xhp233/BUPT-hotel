class AirConditioner:
    def __init__(self, target_temperature=22, billing_rate=1, temperature_change_rate=0.5, max_running=3):
        self.target_temperature = target_temperature
        self.billing_rate = billing_rate
        self.max_runningroom = max_running
        self.temperature_change_rate = temperature_change_rate
        self.rooms = {}
        self.running_rooms = []  # 记录当前正在运行的房间
        self.service_queue = []  # 记录服务队列，服务时长最长的房间
        self.waiting_queue = []  # 记录等待队列

    def add_room(self, room_number, initial_temperature):
        self.rooms[room_number] = {
            'current_temperature': initial_temperature,
            'target_temperature': self.target_temperature,
            'running': True,#启动了空调调度程序
            'fan_speed': 'medium',
            'total_service_time': 0, #总服务时间
            'time_remaining':0,#服务队列里剩余时间
            'current_cost': 0,
            'history': []
        }

    def start_air_conditioning(self, room_number):
        self.rooms[room_number]['running']=True
        self.rooms[room_number]['fan_speed']='medium'
        self.rooms[room_number]['target_temperature']=self.target_temperature
        self.running_rooms.append(room_number)
        self.waiting_queue.append(room_number)

    def set_target_temperature(self, room_number, target_temperature):
        self.rooms[room_number]['target_temperature'] = target_temperature

    def set_fan_speed(self, room_number, fan_speed):
        self.rooms[room_number]['fan_speed'] = fan_speed

    def stop_air_conditioning(self, room_number):
        if room_number in self.running_rooms:
            self.running_rooms.remove(room_number)
        if room_number in self.service_queue:
            self.service_queue.remove(room_number)
        if room_number in self.waiting_queue:
            self.waiting_queue.remove(room_number)

        self.rooms[room_number]['running'] = False

    def update_temperature(self, room_number):
        if self.rooms[room_number]['running']:
            # Determine temperature change rate based on fan speed
            fan_speed = self.rooms[room_number]['fan_speed']
            if fan_speed == 'high':
                temperature_change_rate = 1.0
            elif fan_speed == 'medium':
                temperature_change_rate = 0.5
            elif fan_speed == 'low':
                temperature_change_rate = 0.33
            else:
                # Handle unknown fan speed (optional)
                temperature_change_rate = 0.5

            # Update temperature
            self.rooms[room_number]['current_temperature'] += temperature_change_rate

            # Record history data
            self.rooms[room_number]['history'].append({
                'timestamp': self.rooms[room_number]['time_remaining'],
                'current_temperature': self.rooms[room_number]['current_temperature'],
                'fan_speed': fan_speed
            })


    def calculate_cost(self, room_number, service_time):
        fan_speed_mapping = {'high': 1, 'medium': 2, 'low': 3}
        cost_rate = fan_speed_mapping[self.rooms[room_number]['fan_speed']]
        return service_time * cost_rate * self.billing_rate

    def generate_detailed_invoice(self, room_number):
        # Generate detailed invoice for a room
        pass

    def generate_summary_invoice(self):
        # Generate summary invoice for all rooms
        pass

    
    # def priority_scheduling(self):
    #     # 先将已经达到目标温度的房间移出waiting_queue
    #     remaining_rooms = [room for room in self.waiting_queue if self.rooms[room]['current_temperature'] < self.rooms[room]['target_temperature']]

    #     # 对剩下的房间按照房间温度、风速大小和在等待队列的先后顺序排序
    #     sorted_rooms = sorted(
    #         remaining_rooms,
    #         key=lambda x: (
    #             self.rooms[x]['current_temperature'],
    #             self.rooms[x]['fan_speed'],
    #             self.waiting_queue.index(x)
    #         )
    #     )
    def priority_scheduling(self):
        # 按照房间风速大小和在等待队列的先后顺序排序
        remaining_rooms = [room for room in self.waiting_queue if self.rooms[room]['current_temperature'] < self.rooms[room]['target_temperature']]
        sorted_rooms = sorted(
           remaining_rooms,
            key=lambda x: (self.rooms[x]['fan_speed'], self.waiting_queue.index(x))
        )
        # 将已经达到目标温度的房间添加到排序结果的末尾
        sorted_rooms += [room for room in self.waiting_queue if room not in remaining_rooms]

        if sorted_rooms:
            return sorted_rooms[0]

        return None


    def print_room_status(self):
        for room_number in self.rooms:
            # 输出房间信息
            print(f"Room: {room_number}")
            if room_number in self.running_rooms:
                # 如果房间在运行中，输出目标温度
                print(f"Running: {self.rooms[room_number]['running']}")
                print(f"Target Temperature: {self.rooms[room_number]['target_temperature']}°C")
                if room_number in self.service_queue:
                    # 如果房间在服务队列，输出剩余时间和当前温度                    
                    print(f"Time Remaining: {self.rooms[room_number]['time_remaining']} minutes")
                    

            # 其他情况输出总服务时间和当前温度
            #print(f"Total Service Time: {self.rooms[room_number]['total_service_time']} minutes")
            print(f"Current Temperature: {self.rooms[room_number]['current_temperature']}°C")
            print("------")


if __name__ == '__main__':
    # 示例用法
    ac_system = AirConditioner()

    # 添加房间
    ac_system.add_room('room_one', 10)
    ac_system.add_room('room_two', 15)
    ac_system.add_room('room_three', 18)
    ac_system.add_room('room_four', 12)
    ac_system.add_room('room_five', 14)

    # 模拟运行时长
    for minute in range(1, 27): 
        # 每个循环 输出所有房间信息
        #ac_system.print_room_status()  
        #每个循环 先遍历数据库的请求
        if minute == 1:
            ac_system.start_air_conditioning('room_one')  # 房间一开机
        elif minute == 2:
            ac_system.set_target_temperature('room_one', 24)  # 房间一设置温度
            ac_system.start_air_conditioning('room_two')  # 房间二开机
        elif minute == 3:
            ac_system.start_air_conditioning('room_three')  # 房间三开机
        elif minute == 4:
            ac_system.set_target_temperature('room_two', 25)  # 房间二设置温度
            ac_system.start_air_conditioning('room_four')  # 房间四开机
            ac_system.start_air_conditioning('room_five')  # 房间五开机
        elif minute == 5:
            ac_system.set_target_temperature('room_three', 27)  # 房间三设置温度
            ac_system.set_fan_speed('room_five', 'high')  # 房间五设置风速
        elif minute == 6:
            ac_system.set_fan_speed('room_one', 'high')  # 房间一设置风速
        elif minute == 8:
            ac_system.set_target_temperature('room_five', 24)  # 房间五设置温度
        elif minute == 10:
            ac_system.set_target_temperature('room_one', 28)  # 房间一设置温度
            ac_system.set_fan_speed('room_four', 'high')  # 房间四设置风速
            ac_system.set_target_temperature('room_four', 28)  # 房间四设置温度
        elif minute == 12:
            ac_system.set_fan_speed('room_five', 'medium')  # 房间五设置风速
        elif minute==13:
            ac_system.set_fan_speed('room_two', 'high')  # 房间四二设置风速
        elif minute == 15:
            ac_system.stop_air_conditioning('room_one')  # 房间一关机
            ac_system.set_fan_speed('room_three', 'low')  # 房间三设置风速
        elif minute == 17:
            ac_system.stop_air_conditioning('room_five')  # 房间五关机
        elif minute==18:
            ac_system.set_fan_speed('room_three','high')
        elif minute == 19:
            ac_system.start_air_conditioning('room_one')  # 房间一开机
            ac_system.set_target_temperature('room_four', 25)  # 房间四设置温度
            ac_system.set_fan_speed('room_four', 'medium')  # 房间四设置风速
        elif minute == 21:
            ac_system.set_target_temperature('room_two', 27)  # 房间二设置温度
            ac_system.set_fan_speed('room_two', 'medium')  # 房间二设置风速
            ac_system.start_air_conditioning('room_five')  # 房间五开机
        elif minute == 25:
            ac_system.stop_air_conditioning('room_one')  # 房间一关机
            ac_system.stop_air_conditioning('room_three')  # 房间三关机
            ac_system.stop_air_conditioning('room_five')  # 房间五关机
        elif minute == 26:
            ac_system.stop_air_conditioning('room_two')  # 房间二关机
            ac_system.stop_air_conditioning('room_four')  # 房间四关机

        # Step 1: 运行上一时刻服务队列里的房间，更新温度并减少服务时间
        for room_number in ac_system.service_queue:
            if ac_system.service_queue is not None:
                ac_system.update_temperature(room_number)
                ac_system.rooms[room_number]['time_remaining'] -= 1
        print(f"\nTime 底: {minute}")
        # print("waiting_queue:")
        # for room_number in ac_system.waiting_queue:
        #     print(f"Room: {room_number}") 
        # print("service_queue:")
        # for room_number in ac_system.service_queue:
        #     print(f"Room: {room_number}") 
        # Step 2: 如果服务队列中房间不足3个，使用优先级调度算法将房间加入服务队列

        if len(ac_system.service_queue) < ac_system.max_runningroom :#服务队列里小于三个房间
            if len(ac_system.running_rooms) > ac_system.max_runningroom :#总运行房间大于三个房间
                while len(ac_system.service_queue) < ac_system.max_runningroom:
                    room_to_add = ac_system.priority_scheduling()
                    if room_to_add is not None:
                        ac_system.waiting_queue.remove(room_to_add)
                        ac_system.service_queue.append(room_to_add)
                        ac_system.rooms[room_to_add]['time_remaining'] = 2
                        ac_system.update_temperature(room_to_add)
                        ac_system.rooms[room_to_add]['time_remaining'] -= 1
            else:#总运行房间小于等于三个房间
                while len(ac_system.service_queue) < len(ac_system.running_rooms):
                    room_to_add = ac_system.priority_scheduling()
                    if room_to_add is not None:
                        ac_system.waiting_queue.remove(room_to_add)
                        ac_system.service_queue.append(room_to_add)
                        ac_system.rooms[room_to_add]['time_remaining'] = 2
                        ac_system.update_temperature(room_to_add)
                        ac_system.rooms[room_to_add]['time_remaining'] -= 1
                    if room_to_add is None:
                        break
                    
                        
        # Step 3: 处理房间更改请求，更新房间状态

        for room_number in list(ac_system.service_queue):
            if (ac_system.rooms[room_number][ 'target_temperature'] -ac_system.rooms[room_number]['current_temperature']  <=0.1 ):
                # 房间到达目标温度 退出服务队列
                ac_system.rooms[room_number]['current_temperature']=ac_system.rooms[room_number][ 'target_temperature']
                ac_system.service_queue.remove(room_number)
                ac_system.waiting_queue.append(room_number)
        for room_number in list(ac_system.rooms):
            # 如果房间关机，执行回温
            if not ac_system.rooms[room_number]['running']:
                ac_system.rooms[room_number]['current_temperature'] -= 0.5

        # Step 4: 更新进入等待队列的房间
        for room_number in list(ac_system.service_queue):
            if ac_system.rooms[room_number]['time_remaining'] <= 0:
                # 房间服务时间到，退出服务队列，进入等待队列
                ac_system.service_queue.remove(room_number)
                ac_system.waiting_queue.append(room_number)
        ac_system.print_room_status() 
        print("waiting_queue:")
        for room_number in ac_system.waiting_queue:
            print(f"Room: {room_number}") 
        print("service_queue:")
        for room_number in ac_system.service_queue:
            print(f"Room: {room_number}") 

    print("final_temperature:")   
    ac_system.print_room_status() 