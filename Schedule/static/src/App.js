import React from 'react';
import StickyNavbar from './components/TopNavbar/StickyNavbar';
import VerticalNavbar from './components/VerticalNavbar/VerticalNavbar';
import EmployeeTable from './components/EmployeeTable/EmployeeTable';

const App = () => {
  return (
    <div style={{backgroundColor: '#E4E6F7'}}>
      <StickyNavbar />
      {/* <VerticalNavbar /> */}
      <EmployeeTable />
    </div>
  );
};

export default App;