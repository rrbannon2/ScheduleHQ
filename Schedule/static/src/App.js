import React from 'react';
import StickyNavbar from './components/TopNavbar/StickyNavbar';
// import VerticalNavbar from './components/VerticalNavbar/VerticalNavbar';
// import EmployeeTable from './components/EmployeeTable/EmployeeTable';
// import AddEmployeeTable from './components/AddEmployeeTable/AddEmployeeTable';
// import BaseEmployeeDataTable from './components/BaseEmployeeDataTable/BaseEmployeeDataTable';
// import EditEmployeeDataTable from './components/EditEmployeeDataTable/EditEmployeeDataTable';
// import AddSkillPage from './components/AddSkill/addSkill';
// import EditSkillPage from './components/EditSkill/EditSkill';
// import AddShiftPage from './components/AddShift/AddShift';
// import EditShiftPage from './components/EditShift/EditShift';
import BusinessInfoPage from './components/BusinessInfo/BusinessInfo';
import UpdateBusinessInfo from './components/BusinessInfo/UpdateBusinessInfo';
import BaseDropDownMenu from './components/BaseDropDownMenu/BaseDropDownMenu';

const App = () => {
  return (
    <div style={{backgroundColor: '#E4E6F7'}}>
      <StickyNavbar />
      {/* <VerticalNavbar /> */}
      {/* <EmployeeTable /> */}
      {/* <AddEmployeeTable/> */}
      {/* <BaseEmployeeDataTable /> */}
      {/* <EditEmployeeDataTable dataID={2} /> */}
      {/* <AddSkillPage /> */}
      {/* <EditSkillPage dataID={"TestSkill"} /> */}
      {/* <AddShiftPage /> */}
      {/* <EditShiftPage dataID={"TestShift"} /> */}
      {/* <BusinessInfoPage addNew={false} existingInfo={null} /> */}
      {/* <UpdateBusinessInfo /> */}
      <BaseDropDownMenu URL = "/loadEmployeeNames" />
    </div>
  );
};

export default App;