import sys


class Data:
    def __init__(self, fileName):
        print("Reading input file %s" % fileName)
        self.file = open(fileName, "r")
        self.loadData()
        self.file.close()

    def nextLine(self):
        line = self.file.readline().strip()
        if not line:
            return self.nextLine()
        return line

    def loadData(self):
        self.microservice_count = int(self.nextLine())  # 微服务数量
        self.edgenode_count = int(self.nextLine())  # 边缘节点数量
        self.task_count = int(self.nextLine())  # 任务数量(有多少个f)
        self.T_h_max = float(self.nextLine())  # 任务时延阈值
        self.C_max = float(self.nextLine())  # 微服务放置最大可容忍成本

        self.place_cost = []  # 微服务放置成本
        for i in range(self.microservice_count):
            self.place_cost.append(float(self.nextLine()))

        self.request_resource = []  # 微服务索要的计算资源
        for i in range(self.microservice_count):
            self.request_resource.append(float(self.nextLine()))

        self.data_size_user = float(self.nextLine())  # 用户请求的数据大小

        self.data_size = []  # 对应序号的微服务会输出的数据大小
        for i in range(self.microservice_count):
            self.data_size.append(float(self.nextLine()))

        self.task_user_related_edgenode = []  # 服务该用户的边缘节点序号
        for i in range(self.task_count):
            self.task_user_related_edgenode.append(int(self.nextLine()))

        self.task_dependency = []  # 对应序号任务所依赖的微服务及顺序
        for i in range(self.task_count):
            line = self.nextLine()
            self.task_dependency.append([int(x) for x in line.split()])

        self.r_uovk_user = []  # 用户发送到边缘节点i的传输速率
        for i in range(self.edgenode_count):
            line = self.nextLine()
            self.r_uovk_user.append([int(x) for x in line.split()])

        self.r_uovk = {}  # 边缘节点i到边缘节点j的传输速率
        for i in range(self.edgenode_count):
            line = self.nextLine()
            for j, value in enumerate(line.split()):
                self.r_uovk[(i, j)] = float(value)

        self.c_vk = []  # 边缘节点i的计算资源
        for i in range(self.edgenode_count):
            self.c_vk.append(float(self.nextLine()))

        self.node_capacity = []  # 边缘节点i能够放置微服务的容量
        for i in range(self.edgenode_count):
            self.node_capacity.append(float(self.nextLine()))
