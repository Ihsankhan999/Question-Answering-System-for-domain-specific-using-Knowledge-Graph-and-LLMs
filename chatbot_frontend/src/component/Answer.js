import React from 'react';

export default function Answer({ answer }) {
  return (
    <div className='container d-flex justify-content-end border answer-bg w-50 m-3 p-3'>
      <p>{answer}</p>
    </div>
  );
}
