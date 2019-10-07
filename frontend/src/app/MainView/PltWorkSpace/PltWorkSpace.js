import React from "react";
import PltRow from './PltRow';

class PltWorkSpace extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      "rows_list": [1, 2, 3, 4, 5],
      "classes": "col-12 col-md-9 col-xl-8",
      "styles": {"marginTop": "7rem", "marginLeft": "16rem", "zIndex": 0}
    }
  }

  render() {
    return (
      <main role="main" className={this.state.classes} style={this.state.styles}>
        <table className={"bg-light table-bordered"}>
          <tbody>
          {
            this.state.rows_list.map(
              (number) => {
                return <PltRow rowPosition={number} key={number}/>
              })
          }
          </tbody>
        </table>
      </main>
    )
  }
}

export default PltWorkSpace;