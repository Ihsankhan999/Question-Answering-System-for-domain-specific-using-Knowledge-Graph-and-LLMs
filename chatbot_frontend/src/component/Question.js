import React from 'react';

function Question({ question }) {
  return (
    <div className='container w-50 m-3 p-3 question'>
      <p>{question}</p>
    </div>
  );
}

export default Question;
