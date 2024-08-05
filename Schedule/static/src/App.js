import React from 'react';
import StickyNavbar from './components/TopNavbar/StickyNavbar';
import EmployeeTable from './components/EmployeeTable/EmployeeTable';
import AddEmployeeTable from './components/AddEmployeeTable/AddEmployeeTable';
import BaseEmployeeDataTable from './components/BaseEmployeeDataTable/BaseEmployeeDataTable';
import EditEmployeeDataTable from './components/EditEmployeeDataTable/EditEmployeeDataTable';
import AddSkillPage from './components/AddSkill/addSkill';
import EditSkillPage from './components/EditSkill/EditSkill';
import AddShiftPage from './components/AddShift/AddShift';
import EditShiftPage from './components/EditShift/EditShift';
import BusinessInfoPage from './components/BusinessInfo/BusinessInfo';
import SignUpPage from './components/SignUpPage/SignUpPage';
import UpdateBusinessInfo from './components/BusinessInfo/UpdateBusinessInfo';
import LoginPage from './components/LoginPage/LoginPage';
import DisplaySchedulePage from './components/DisplaySchedule/DisplaySchedulePage';
import ShiftsTable from './components/ShiftsTable/ShiftsTable';
import SkillsTable from './components/SkillsTable/SkillsTable';
import LoggedOutNavbar from './components/LoggedOutNavbar/LoggedOutNavbar';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

const App = () => {
  return (
    <div style={{ backgroundColor: '#E4E6F7' }}>
      <Router>
        <StickyNavbar />
        
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/home" element={<DisplaySchedulePage />} />
          <Route path="/employeetable" element={<EmployeeTable />} />
          <Route path="/addemptable" element={<AddEmployeeTable />} />
          <Route path="/editemptable" element={<EditEmployeeDataTable />} />
          <Route path="/addskill" element={<AddSkillPage />} />
          <Route path="/editskill" element={<EditSkillPage />} />
          <Route path="/addshift" element={<AddShiftPage />} />
          <Route path="/editshift" element={<EditShiftPage />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/businessinfo" element={<BusinessInfoPage addNew={false} existingInfo={null} />} />
          <Route path="/updatebusinessinfo" element={<UpdateBusinessInfo />} />
          <Route path="/shiftstable" element={<ShiftsTable />} />
          <Route path="/skillstable" element={<SkillsTable />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;