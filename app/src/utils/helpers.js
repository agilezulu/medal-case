export const round = (value, precision) => {
  const multiplier = Math.pow(10, precision || 0);
  return Math.round(value * multiplier) / multiplier;
}

export const getDate = (datetime) => datetime.split('T')[0];
export const metersToDistanceUnits = (meters, units) => round(meters * 0.000621371, 1);

export const secsToHMS = (seconds) => new Date(seconds * 1000).toISOString().slice(11, 19);
