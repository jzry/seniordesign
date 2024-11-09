import React from 'react';
import '../../styles/CTRHandWritingRecognitionStyles.css';

function BCEResults({ extractedDataList, fastestRiderTime, heaviestRiderWeight }) {
  const calculateVeterinaryScore = (data) => {
    const { Recovery, Hydration, Lesions, Soundness, 'Qual Mvmt': QualMvmt } = data;
    return (parseFloat(Recovery.value, 10) + parseFloat(Hydration.value, 10) + parseFloat(Lesions.value, 10) + parseFloat(Soundness.value, 10) + parseFloat(QualMvmt.value, 10)) * 10;
  };

  const calculateWeightScore = (weight) => {
    return 100 - (heaviestRiderWeight - weight) / 2;
  };

  const calculateTimeScore = (rideTime) => {
    // Convert the three-digit time values to hours and minutes format if necessary
    const fastestTimeInMinutes = convertToMinutes(fastestRiderTime);
    const rideTimeInMinutes = convertToMinutes(rideTime);

    // Calculate time score
    return 200 - (rideTimeInMinutes - fastestTimeInMinutes);
  };

  const convertToMinutes = (time) => {
    // Convert time to hours and minutes format
    const hours = Math.floor(time / 100);
    const minutes = time % 100;
    return hours * 60 + minutes;
  };

  return (
    <div className="container">
      {extractedDataList.map((data, index) => {
        const totalVeterinaryScore = calculateVeterinaryScore(data);
        const totalWeightScore = calculateWeightScore(parseInt(data['Weight of this rider'].value, 10));
        const totalTimeScore = calculateTimeScore(parseInt(data['Ride time, this rider'].value, 10));

        return (
          <div key={index} className="bce-result">
            <h4>Rider number: {data['Rider number'].value}</h4>
            <p>Total Veterinary Score: {totalVeterinaryScore}</p>
            <p>Total Time Score: {totalTimeScore}</p>
            <p>Total Weight Score: {totalWeightScore}</p>
            <h3>Total Score: {totalVeterinaryScore + totalWeightScore + totalTimeScore}</h3>
            <p>-----------</p>
          </div>
        );
      })}
      <button className="action-button" onClick={() => window.location.reload()}>Calculate New Score</button>
    </div>
  );
}

export default BCEResults;
