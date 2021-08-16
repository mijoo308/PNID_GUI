class BoxModel:
    def __init__(self, parsed_data):
        super().__init__()
        self.data = parsed_data
        self.selectedDataIndex = None
        # string, orientation, xmin, ymin, xmax, ymax, visible

    #     self.row = self.data.shape[0]
    #     self.col = self.data.shape[1]
    #
    #     self.model = QStandardItemModel()
    #     for i in range(self.col):
    #         self.model.appendRow(self.data[:, i])

    def setLayerSignal(self, notify_selected_to_layer, notify_deleted_to_layer, notify_edited_to_layer):
        self.notify_selected_to_layer = notify_selected_to_layer
        self.notify_deleted_to_layer = notify_deleted_to_layer
        self.notify_edited_to_layer = notify_edited_to_layer

    def setTableSignal(self, notify_selected_to_table, notify_added_to_table):
        self.notify_selected_to_table = notify_selected_to_table
        self.notify_added_to_table = notify_added_to_table

    def deleteBox(self, i):
        del self.data[i]
        self.notify_deleted_to_layer(i)

    def setSelectedDataIndex(self, index, flag):  # flag = 0 : to table/ 1: to layer
        self.selectedDataIndex = index
        if flag == 0:
            self.notify_selected_to_table(self.selectedDataIndex)
        elif flag == 1:
            self.notify_selected_to_layer(self.selectedDataIndex)

    def getBoxData(self, idx=None):
        if idx is None:
            return self.data
        else:
            return self.data[idx]

    def setBoxData(self, i, new_data):
        prev_data = self.data[i].copy()
        self.data[i] = new_data

        bndbox_ischanged = False
        for bndbox_idx in range(2, 6):  # box 좌표가 바뀌었으면
            if prev_data[bndbox_idx] != new_data[bndbox_idx]:
                bndbox_ischanged = True
                break
        if bndbox_ischanged:
            self.notify_edited_to_layer(i, new_data)

    def addBoxData(self, new_bndbox):
        xmin = new_bndbox[0]
        ymin = new_bndbox[1]
        xmax = new_bndbox[2]
        ymax = new_bndbox[3]
        string = ''
        orientation = 0

        if ymax - ymin > xmax - xmin: orientation = 90

        new_row = ['', string, xmin, ymin, xmax, ymax, orientation]
        # self.data = np.append(self.data, new_row, axis=1) # np제거
        self.data.append(new_row)

        self.notify_added_to_table()