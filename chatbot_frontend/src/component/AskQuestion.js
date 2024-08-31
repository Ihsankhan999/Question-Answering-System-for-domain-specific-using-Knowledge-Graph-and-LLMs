import React, { useRef } from 'react';
import { Container, Row, Col, Form, InputGroup } from 'react-bootstrap';
import axios from 'axios';

export default function AskQuestion({ onQuestionSubmit }) {
  const inputRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const question = inputRef.current.value;

    try {
      await axios.post('http://127.0.0.1:8000/chatbot/get_question/', { question });
      onQuestionSubmit(question); 
      inputRef.current.value = ''; 
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  return (
    <Container className="chat-container">
      <Row>
        <Col>
          <Form onSubmit={handleSubmit}>
            <Form.Group as={Row} className="input-container">
              <Col xs={9}>
                <div className='input-col'>
                  <InputGroup  className='input'>
                    <Form.Control
                     
                      type="text"
                      name="question"
                      placeholder="Type your message..."
                      ref={inputRef} // Assign the ref to the input field
                    />
                  </InputGroup>
                </div>
              </Col>
              <Col xs={3}>
                <div className='btn-col'>
                  <button type='submit' className="send-button">Send</button>
                </div>
              </Col>
            </Form.Group>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}
