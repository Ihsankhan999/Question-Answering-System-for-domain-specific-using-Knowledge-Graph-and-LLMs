import React, { useState } from "react";
import Question from "./Question";
import Answer from "./Answer";
import AskQuestion from "./AskQuestion";
import axios from "axios";
import Cover from './KG.jpeg'
import Loader from "./Loader";
export default function Chatbot() {
  const [qaPairs, setQaPairs] = useState([]); // Combined state for questions and answers
  const [showWelcomeMessage, setShowWelcomeMessage] = useState(true);

  const handleQuestionSubmit = async (question) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chatbot/get_question/",
        { question }
      );
      const newAnswer = response.data.answer[0];
      setQaPairs([...qaPairs, { question, answer: newAnswer }]);
      setShowWelcomeMessage(false); // Hide welcome message after submitting a question
    } catch (error) {
      console.error("Error submitting question:", error);
    }
  };

  return (
    <div className="Container mt-3">
      <div className="row d-flex align-items-center flex-column m-0 ">
        <div className="col col-sm-12 col-lg-10 col-md-10 Container-color p-4 shadow">
          <div className="chat-bot">
            {/* <Loader/>\\ */}
            {showWelcomeMessage ? (
              <div className="d-flex justify-content-center align-items-center img-container rounded">
              <img src={Cover} alt="cover" className="img-fluid img-cover " />
            </div>
            
            ) : (
              <div className="qa-pairs">
                {qaPairs.map((pair, index) => (
                  <div key={index}>
                    <div className="question-send">
                      <Question question={pair.question} />
                    </div>
                    <div className="answer">
                      <Answer answer={pair.answer} />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
      <div className="ask-question">
        <AskQuestion onQuestionSubmit={handleQuestionSubmit} />
      </div>
    </div>
  );
}
