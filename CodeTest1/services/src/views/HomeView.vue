<template>
  <v-container>
    <v-row>
      <v-col cols="auto">
        <v-btn color="light-green darken-1" dark @click="openAddDialog">
          Add
        </v-btn>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="auto" class="text-right">
        <v-btn color="amber darken-2" dark class="mr-2" @click="downloadExcel"
          >Download</v-btn
        >
        <v-btn color="amber darken-2" dark @click="$refs.fileInput.click()">
          Upload
          <input
            ref="fileInput"
            type="file"
            accept=".xlsx"
            style="display: none"
            @change="handleFileUpload"
          />
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-data-table
          :headers="headers"
          :items="rows"
          item-key="part_no"
          class="elevation-1 custom-table"
          hide-default-header
        >
          <template v-slot:header>
            <tr>
              <th
                v-for="(header, index) in headers"
                :key="header.value"
                :class="index === 0 ? 'green-header' : 'yellow-header'"
              >
                {{ header.text }}
              </th>
            </tr>
          </template>
          <template v-slot:item="{ item }">
            <tr>
              <td
                v-for="(header, index) in headers"
                :key="header.value"
                :class="getRowCellClass(item[header.value], index)"
              >
                {{ item[header.value] === "dense" ? "" : item[header.value] }}
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <!-- Dialog สำหรับเพิ่ม Part_NO ใหม่ -->
    <v-dialog v-model="addDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title>
          <span class="headline">Add New Part</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeAddDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="newPartNo"
            label="New Part NO"
            @keyup.enter="checkPartNo"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeAddDialog">
            Cancel
          </v-btn>
          <v-btn color="blue darken-1" text @click="checkPartNo">Add</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog สำหรับกำหนดเวลาและความสัมพันธ์ -->
    <v-dialog v-model="timeDialog" max-width="500px" persistent>
      <v-card>
        <v-card-title>
          <span class="headline">Set Time for New Part</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeTimeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-select
            v-if="availableRelations.length > 0"
            v-model="selectedRelations"
            :items="availableRelations"
            item-text="label"
            item-value="value"
            multiple
            chips
            label="Select Relations"
          ></v-select>
          <v-text-field
            v-if="availableRelations.length > 0"
            v-model.number="newTime"
            label="Time"
            type="number"
            :rules="[(v) => v > 0 || 'Time must be greater than 0']"
            @keyup.enter="addRelation"
          ></v-text-field>
          <v-list class="relation-list" max-height="150">
            <v-list-item
              v-for="relation in sortedSavedRelations"
              :key="`${relation.start_part_no}-${relation.end_part_no}`"
            >
              <v-list-item-content>
                {{ relation.start_part_no }} -> {{ relation.end_part_no }} :
                {{ relation.time }}
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-btn
            v-if="availableRelations.length > 0"
            color="blue darken-1"
            text
            @click="addRelation"
          >
            Add Relation
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeTimeDialog">
            Cancel
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="saveNewPart"
            :disabled="!allRelationsSelected"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "HomeView",
  data() {
    return {
      headers: [],
      rows: [],
      addDialog: false,
      timeDialog: false,
      newPartNo: "",
      existingParts: [],
      selectedRelations: [],
      availableRelations: [],
      savedRelations: [],
      newTime: null,
      allRelationsOrder: [],
    };
  },
  computed: {
    allRelationsSelected() {
      return (
        this.availableRelations.length === 0 && this.savedRelations.length > 0
      );
    },
    sortedSavedRelations() {
      return [...this.savedRelations].sort((a, b) => {
        const indexA = this.allRelationsOrder.findIndex(
          (r) => r.start === a.start_part_no && r.end === a.end_part_no
        );
        const indexB = this.allRelationsOrder.findIndex(
          (r) => r.start === b.start_part_no && r.end === b.end_part_no
        );
        return indexA - indexB;
      });
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      const path = "http://localhost:8000/parts-with-times/";
      try {
        const response = await axios.get(path);
        //console.log("API Response:", response.data);
        if (response.data && response.data.headers && response.data.rows) {
          this.headers = response.data.headers.map((header) => ({
            text: header.text,
            value: header.value,
            align: "center",
            sortable: false,
          }));
          this.rows = response.data.rows;
          //console.log("Headers:", this.headers);
          //console.log("Rows:", this.rows);
        } else {
          //console.error("Invalid data structure from API");
        }
      } catch (error) {
        //console.error("Error fetching data:", error);
      }
    },
    getRowCellClass(value, index) {
      if (index === 0) return "yellow-cell";
      if (value === "dense") return "dense-cell";
      return "white-cell";
    },
    openAddDialog() {
      this.addDialog = true;
    },
    closeAddDialog() {
      this.addDialog = false;
      this.newPartNo = "";
    },
    closeTimeDialog() {
      this.timeDialog = false;
      this.selectedRelations = [];
      this.newTime = null;
      this.savedRelations = [];
      this.newPartNo = "";
    },
    async checkPartNo() {
      const isDuplicate = this.rows.some(
        (row) => row.part_no === this.newPartNo
      );
      if (isDuplicate) {
        alert("Part NO already exists. Please enter a new one.");
      } else {
        this.addDialog = false;
        this.existingParts = this.rows.map((row) => row.part_no);
        this.prepareRelations();
        this.timeDialog = true;
      }
    },
    prepareRelations() {
      this.allRelationsOrder = [
        ...this.existingParts.map((part) => ({
          start: part,
          end: this.newPartNo,
        })),
        ...this.existingParts.map((part) => ({
          start: this.newPartNo,
          end: part,
        })),
      ];

      this.availableRelations = this.allRelationsOrder.map((relation) => ({
        label: `${relation.start} -> ${relation.end}`,
        value: relation,
      }));
    },
    addRelation() {
      if (
        this.selectedRelations.length > 0 &&
        this.newTime &&
        this.newTime > 0
      ) {
        this.selectedRelations.forEach((relation) => {
          this.savedRelations.push({
            start_part_no: relation.start,
            end_part_no: relation.end,
            time: parseFloat(this.newTime),
          });
        });
        this.removeAddedRelations();
        this.selectedRelations = [];
        this.newTime = null;
      } else {
        if (!this.newTime || this.newTime <= 0) {
          alert("Please enter a valid time greater than 0.");
        } else {
          alert("Please select relations and enter a valid time.");
        }
      }
    },
    removeAddedRelations() {
      this.availableRelations = this.availableRelations.filter(
        (relation) =>
          !this.selectedRelations.some(
            (selected) =>
              selected.start === relation.value.start &&
              selected.end === relation.value.end
          )
      );
    },
    async saveNewPart() {
      try {
        await axios.post("http://localhost:8000/add-new-part/", {
          new_part_no: this.newPartNo,
          part_relations: this.savedRelations,
        });

        await this.fetchData();

        this.closeTimeDialog();
      } catch (error) {
        console.error("Error adding new part:", error);
        alert("Failed to add new part. Please try again.");
      }
    },
    async downloadExcel() {
      try {
        const response = await axios.get(
          "http://localhost:8000/download-excel/",
          {
            responseType: "blob",
          }
        );

        const contentDisposition = response.headers["content-disposition"];
        let fileName = "parts_change_over_matrix.xlsx";
        if (contentDisposition) {
          const fileNameMatch = contentDisposition.match(/filename="?(.+)"?/i);
          if (fileNameMatch.length === 2) fileName = fileNameMatch[1];
        }

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", fileName);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error("Error downloading Excel file:", error);
        alert("Failed to download Excel file. Please try again.");
      }
    },
    async handleFileUpload(event) {
      const file = event.target.files[0];
      if (
        file &&
        file.type ===
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      ) {
        const formData = new FormData();
        formData.append("file", file);

        try {
          const response = await axios.post(
            "http://localhost:8000/upload-excel/",
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          );

          // ตรวจสอบการตอบกลับจาก API
          if (response.data && response.data.message) {
            alert(response.data.message);
          } else {
            alert("Excel file uploaded successfully.");
          }

          // รีเฟรชข้อมูลหลังจากอัปโหลด
          await this.fetchData();
        } catch (error) {
          console.error("Error uploading Excel file:", error);
          if (
            error.response &&
            error.response.data &&
            error.response.data.detail
          ) {
            alert(`Failed to upload Excel file: ${error.response.data.detail}`);
          } else {
            alert("Failed to upload Excel file. Please try again.");
          }
        }

        // รีเซ็ต input file หลังการอัปโหลด
        this.$refs.fileInput.value = "";
      } else {
        alert("Please select a valid Excel file.");
      }
    },
  },
};
</script>

<style scoped>
.custom-table {
  border-collapse: collapse;
}
.custom-table >>> th,
.custom-table >>> td {
  border: 1px solid #b0b0b0;
  text-align: center !important;
  padding: 8px;
}
.green-header {
  background-color: #c3f1c4 !important;
  color: #2c3e50 !important;
  font-size: 16px;
  font-weight: bold;
}
.yellow-header {
  background-color: #fff6a1 !important;
  color: #2c3e50 !important;
  font-size: 16px;
  font-weight: bold;
}
.yellow-cell {
  background-color: #fffbe6;
}
.white-cell {
  background-color: #ffffff;
}
.dense-cell {
  background-color: #65696b;
  color: #ffffff;
}
.v-btn {
  text-transform: none;
}
.relation-list {
  max-height: 150px;
  overflow-y: auto;
}
</style>
