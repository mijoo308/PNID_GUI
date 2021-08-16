
class TableViewModel:
    def __init__(self, data_model, view):
        super().__init__()

        # 모델 객체 이용 (모델)
        self.model = data_model
        self.selectedIndex = None
        # self.data = self.model.getData()
        # self.boxModel = BoxModel(self.data)

        # 처음엔 원본xml로 초기화 (뷰)
        self.tableView = view
        self.tableView.setSignal(on_data_changed_from_view=self.getChagedDataFromView, get_data_func=self.getBoxData,
                                 notify_selected_index=self.notify_selected_index,
                                 notify_deleted_index=self.notify_deleted_index)
        self.model.setTableSignal(notify_selected_to_table=self.get_selected_index,
                                  notify_added_to_table=self.get_added_box)
        self.tableView.setInitData()
        self.tableView.IsInitialized = True

    def getChagedDataFromView(self, row, value):
        self.updateBoxData(row, value)

        print(row, value, "is changed")  # test
        # box 그리는 것도 추가해야함

    def getBoxData(self):
        return self.model.getBoxData()

    def updateBoxData(self, i, newData):
        self.model.setBoxData(i, newData)

    def get_selected_index(self, i):
        self.selectedIndex = i
        self.tableView.selectionChange(self.selectedIndex)

    def get_added_box(self):
        added_data = self.model.getBoxData(idx=-1).copy()
        self.tableView.addTableCell(added_data)
        # table view에 업데이트

    def notify_selected_index(self, i):
        self.model.setSelectedDataIndex(i, 1)

    def notify_deleted_index(self, i):
        self.model.deleteBox(i)
