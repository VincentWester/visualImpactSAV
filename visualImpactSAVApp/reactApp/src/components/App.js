import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";

const App = () => (
  <DataProvider endpoint="/visualImpactSAV/api/dossiers_sav/" 
                render={data => <Table data={data} />} />
);

export default App