import React, {Fragment} from "react";
import {Modal, Button, Form} from 'react-bootstrap';

import {AppMethodsContext, AppStateContext, ProjectContext} from '../Context/ProjectContext';


export default class EditPltButtonModalView extends React.Component {
  static contextType = AppStateContext;

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
                        Редактирование кнопки
                      </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>

                      {appState.edit.show && <Editor button={appState.edit.button}/>}

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


class Editor extends React.Component {
  constructor(props) {
    super(props);

    this.state = {}
  }

  render() {
    let title = this.props.button ? (this.props.button['title'].split('/n').join('\n')) : ('');

    return (
      <Form>
        <Form.Group controlId="exampleForm.ControlTextarea1">
          <Form.Label>Текст на кнопке</Form.Label>
          <Form.Control as="textarea" rows="7" value={title}/>
        </Form.Group>
      </Form>
    )
  }
}