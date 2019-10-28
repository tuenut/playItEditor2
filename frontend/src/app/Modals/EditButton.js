import React from "react";
import {Modal, Button} from 'react-bootstrap';

import {AppMethodsContext, AppStateContext, ProjectContext} from '../Context/ProjectContext';


export default class EditPltButtonModalView extends React.Component {
  render() {
    return (
      <AppMethodsContext.Consumer>
        {({appMethods}) => (
          <AppStateContext.Consumer>
            {({appState}) => (
              <ProjectContext.Consumer>
                {({projectState}) => (

                  <Modal show={appState.edit.show} onHide={appMethods.closeEditPltButtonModal} size={"lg"} centered>
                    <Modal.Header closeButton>
                      <Modal.Title>
                        {appState.edit.title}
                      </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                      {appState.edit.body}
                    </Modal.Body>
                    <Modal.Footer>
                      <Button variant="secondary" onClick={appMethods.closeEditPltButtonModal}>
                        Close
                      </Button>
                    </Modal.Footer>
                  </Modal>

                )}
              </ProjectContext.Consumer>
            )}
          </AppStateContext.Consumer>
        )}
      </AppMethodsContext.Consumer>
    )
  }
}