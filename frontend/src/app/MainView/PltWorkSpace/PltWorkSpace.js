import React from "react";
import PltButton from "./PltButton";


export default function PltWorkSpace() {
  let mainStyle = {
    "marginTop": "7rem",
    "marginLeft": "16rem",
    "zIndex": 0
  }

  return (
    <main role="main" className={"col"} style={mainStyle}>
      {/*<AppStateContext.Consumer>*/}
        {/*{({appState}) => (appState.currentMacros &&*/}
          {/*<AppMethodsContext.Consumer>*/}
            {/*{({appMethods}) => (*/}
              {/*<PltTable*/}
                {/*macros={appState.currentMacros} getButton={appMethods.getButton} getMacros={appMethods.getMacros}*/}
              {/*/>*/}
            {/*)}*/}
          {/*</AppMethodsContext.Consumer>*/}
        {/*)}*/}
      {/*</AppStateContext.Consumer>*/}
    </main>
  )
}


function PltTable({macros, getButton, getMacros}) {
  /* range generator from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from#Sequence_generator_range */
  const range = (start, stop, step) => Array.from({length: (stop - start) / step + 1}, (_, i) => start + (i * step));

  let macros_object = getMacros(macros);
  let rows = range(1, Number(macros_object["Ctrl"]["rows"]), 1);
  let cols = range(1, Number(macros_object["Ctrl"]["columns"]), 1);

  return (
    <table className={"table-bordered"}>
      <tbody>
      {rows.map((row) =>
        <tr key={row}>
          {cols.map((col) =>
            <td className={"m-0 p-0"} key={`${row}.${col}`}>
              <PltButton config={getButton(row, col, macros)} position={[row, col]}/>
            </td>
          )}
        </tr>
      )}
      </tbody>
    </table>
  )
}
