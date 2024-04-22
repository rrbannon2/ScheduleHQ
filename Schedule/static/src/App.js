import React from 'react';
import StickyNavbar from './components/TopNavbar/StickyNavbar';
// import VerticalNavbar from './components/VerticalNavbar/VerticalNavbar';
import EmployeeTable from './components/EmployeeTable/EmployeeTable';
import AddEmployeeTable from './components/AddEmployeeTable/AddEmployeeTable';
import BaseEmployeeDataTable from './components/BaseEmployeeDataTable/BaseEmployeeDataTable';
import EditEmployeeDataTable from './components/EditEmployeeDataTable/EditEmployeeDataTable';
import AddSkillPage from './components/AddSkill/addSkill';
import EditSkillPage from './components/EditSkill/EditSkill';
import AddShiftPage from './components/AddShift/AddShift';
import EditShiftPage from './components/EditShift/EditShift';
import BusinessInfoPage from './components/BusinessInfo/BusinessInfo';
import UpdateBusinessInfo from './components/BusinessInfo/UpdateBusinessInfo';
import BaseDropDownMenu from './components/BaseDropDownMenu/BaseDropDownMenu';
import DisplaySchedulePage from './components/DisplaySchedule/DisplaySchedulePage';
import ShiftsTable from './components/ShiftsTable/ShiftsTable';
import SkillsTable from './components/SkillsTable/SkillsTable';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

const App = () => {
  return (
    <div style={{ backgroundColor: '#E4E6F7' }}>
      <Router>
        <StickyNavbar />
        {/* <VerticalNavbar /> */}
        {/* <AddEmployeeTable/> */}
        {/* <BaseEmployeeDataTable /> */}
        {/* <EditEmployeeDataTable dataID={2} /> */}
        {/* <AddSkillPage /> */}
        {/* <EditSkillPage dataID={"TestSkill"} /> */}
        {/* <AddShiftPage /> */}
        {/* <EditShiftPage dataID={"TestShift"} /> */}
        {/* <BusinessInfoPage addNew={false} existingInfo={null} /> */}
        {/* <UpdateBusinessInfo /> */}
        
        <Routes>
          <Route path="/" element={<DisplaySchedulePage />} />
          <Route path="/employeetable" element={<EmployeeTable />} />
          <Route path="/addemptable" element={<AddEmployeeTable />} />
          <Route path="/baseemptable" element={<BaseEmployeeDataTable />} />
          <Route path="/editemptable" element={<EditEmployeeDataTable />} />
          <Route path="/addskill" element={<AddSkillPage />} />
          <Route path="/editskill" element={<EditSkillPage />} />
          <Route path="/addshift" element={<AddShiftPage />} />
          <Route path="/editshift" element={<EditShiftPage />} />
          <Route path="/businessinfo" element={<BusinessInfoPage addNew={false} existingInfo={null} />} />
          <Route path="/updatebusinessinfo" element={<UpdateBusinessInfo />} />
          <Route path="/dropdownmenu" element={<BaseDropDownMenu URL="/loadEmployeeListData" />} />
          <Route path="/shiftstable" element={<ShiftsTable />} />
          <Route path="/skillstable" element={<SkillsTable />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;