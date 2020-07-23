import React from 'react';
import logo from './logo.svg';
import './App.css';

import {
  Container,
  Row,
  Col,
  Button,
  Form,
  Modal
} from 'react-bootstrap';
import axios from 'axios';

function App() {

  let [ file, setFile] = React.useState(null);
  let [ result, setResult ] = React.useState("");

  const [show, setShow] = React.useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const onFileChange = (event) => {
    console.log(event.target.files[0])
    setFile(event.target.files[0]);
  }

  const onClickShowResults = async () => {
    let data = new FormData();
    data.append('image', file)
    axios.post("http://localhost:5000/predict_html", data)
      .then(res => {
        console.log(res);
        setResult(res.data)
      })

  }

  return (
    <div className="App">
      <Container>
        <Row>
          <Col>
            <Form>
              <Form.Group>
                <Form.File onChange={(event) => {onFileChange(event)}}/>
              </Form.Group>
              <Button onClick={() => {onClickShowResults()}}>Show results</Button>
              <Button onClick={handleShow}>Show modal</Button>
            </Form>
          </Col>
        </Row>
      </Container>
      <Container dangerouslySetInnerHTML={{__html: String(result)}}>
      </Container>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Modal heading</Modal.Title>
        </Modal.Header>
        <Modal.Body dangerouslySetInnerHTML={{__html: String(result)}}/>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleClose}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default App;
