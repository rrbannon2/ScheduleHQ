import React from 'react';
import StickyNavbar from './components/TopNavbar/StickyNavbar';
import VerticalNavbar from './components/VerticalNavbar/VerticalNavbar';
import EmployeeTable from './components/EmployeeTable/EmployeeTable';
import AddEmployeeTable from './components/AddEmployeeTable/AddEmployeeTable';
import BaseEmployeeDataTable from './components/BaseEmployeeDataTable/BaseEmployeeDataTable';
import EditEmployeeDataTable from './components/EditEmployeeDataTable/EditEmployeeDataTable';

const App = () => {
  return (
    <div style={{backgroundColor: '#E4E6F7'}}>
      <StickyNavbar />
      {/* <VerticalNavbar /> */}
      {/* <EmployeeTable /> */}
      <AddEmployeeTable/>
      {/* <BaseEmployeeDataTable /> */}
      <EditEmployeeDataTable employeeName={1} />
    </div>
  );
};

export default App;