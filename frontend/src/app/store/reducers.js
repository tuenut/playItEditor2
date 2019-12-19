import { combineReducers } from "redux";

import { projectReducer } from "./App/reducers";
import {openFileReducer} from './App/TopPaneView/OpenFile/reducers';

export default combineReducers({
  project: projectReducer,
  navbar: openFileReducer
});