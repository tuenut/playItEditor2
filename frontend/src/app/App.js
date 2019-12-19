import React from 'react';
import { createStore } from "redux";
import { Provider } from "react-redux";

// import MainView from './components/MainView/MainView';
import NavigationBar from './components/TopPaneView/NavigationBar';
// import ErrorModal from './Modals/Error';
// import EditPltButtonModalView from './Modals/EditButton';
import reducer from "./store/reducers";

const store = createStore(reducer);


class App extends React.Component {
  render() {
    return (

      <div className={"container-fluid"}>
        <div className={"row flex-xl-nowrap"}>
          <Provider store={store}>

          <NavigationBar/>

          {/*<MainView/>*/}

          {/*<ErrorModal/>*/}
          {/*<EditPltButtonModalView/>*/}
          </Provider>
        </div>
      </div>

    )
  }
}

export default App;
