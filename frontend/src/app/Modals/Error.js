import React, {Fragment} from "react";
import {Modal, Button} from 'react-bootstrap';

import {AppMethodsContext, AppStateContext} from '../Context/ProjectContext';


export default class ErrorModal extends React.Component {
  render() {
    return (
      <AppMethodsContext.Consumer>
        {({appMethods}) => (
          <AppStateContext.Consumer>
            {({appState}) => (

              <Modal show={appState.error.show} onHide={appMethods.closeError}>
                <Modal.Header closeButton>
                  <Modal.Title>
                    {appState.error.title}
                  </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                  {appState.error.body}
                </Modal.Body>
                <Modal.Footer>
                  <Button variant="secondary" onClick={appMethods.closeError}>
                    Close
                  </Button>
                </Modal.Footer>
              </Modal>

            )}
          </AppStateContext.Consumer>
        )}
      </AppMethodsContext.Consumer>
    )
  }
}

