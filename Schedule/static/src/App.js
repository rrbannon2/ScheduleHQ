import React from 'react';
import StickyNavbar from './components/TopNavbar/StickyNavbar';
import VerticalNavbar from './components/VerticalNavbar/VerticalNavbar';
import EmployeeTable from './components/EmployeeTable/EmployeeTable';
import AddEmployeeTable from './components/AddEmployeeTable/AddEmployeeTable';
const App = () => {
  return (
    <div style={{backgroundColor: '#E4E6F7'}}>
      <StickyNavbar />
      {/* <VerticalNavbar /> */}
      {/* <EmployeeTable /> */}
      <AddEmployeeTable />
    </div>
  );
};

export default App;