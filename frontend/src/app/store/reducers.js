import { combineReducers } from "redux";

import { appLevelReducer } from "./App/reducers";
import {navbarLevelReducer} from './App/TopPaneView/OpenFile/reducers';

export default combineReducers({
  app: appLevelReducer,
  navbar: navbarLevelReducer
});