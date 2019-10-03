import React from "react";

class SidePane extends React.Component {
  render() {
    return (
      <nav className="col border-right border-dark bg-light"
           style={{
             "height": "100%",
             "margin-top": "4rem",
             "position": "fixed",
             "width": "16rem",
             "zIndex": 1000
           }}
      >

        <div className="d-flex flex-column my-3 d-xs-none">
        </div>

      </nav>
    )
  }

}

export default SidePane;