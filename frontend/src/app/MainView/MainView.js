import React from 'react';
import PltWorkSpace from './PltWorkSpace';

class MainView extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <main role="main" className="col-12 col-md-9 col-xl-8"
            style={{
              "margin-top": "7rem",
              "margin-left": "16rem",
              "zIndex": 0
            }}
      >
        <PltWorkSpace/>
      </main>
    )
  }
}

export default MainView;