import React from 'react';
import '../../styles/CTRHandWritingRecognitionStyles.css';

function BCEResults({ extractedDataList, heaviestRiderWeight }) {
  const calculateVeterinaryScore = (data) => {
    const { Recovery, Hydration, Lesions, Soundness, 'Qual Mvmt': QualMvmt } = data;
    return (parseInt(Recovery.value, 10) + parseInt(Hydration.value, 10) + parseInt(Lesions.value, 10) + parseInt(Soundness.value, 10) + parseInt(QualMvmt.value, 10)) * 10;
  };

  const calculateWeightScore = (weight) => {
    return 100 - (heaviestRiderWeight - weight) / 2;
  };

  return (
    <div className="container">
      {extractedDataList.map((data, index) => {
        const totalVeterinaryScore = calculateVeterinaryScore(data);
        const totalWeightScore = calculateWeightScore(parseInt(data['Weight of this rider'].value, 10));

        return (
          <div key={index} className="bce-result">
            <h4>Rider number: {data['Rider number'].value}</h4>
            <p>Total Veterinary Score: {totalVeterinaryScore}</p>
            <p>Total Time Score: ?</p>
            <p>Total Weight Score: {totalWeightScore}</p>
            <h3>Total Score: ?</h3>
            <p>-----------</p>
          </div>
        );
      })}
      <button className="action-button" onClick={() => window.location.reload()}>Calculate New Score</button>
    </div>
  );
}

export default BCEResults;
