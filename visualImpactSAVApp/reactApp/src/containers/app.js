import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "../components/DataProvider";
import Table from "../components/Table";

const App = () => (
    <DataProvider endpoint="/visualImpactSAV/api/dossiers_sav/" 
                  render={data => <Table data={data} />} />
);

export default App