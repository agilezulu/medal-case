export const round = (value, precision) => {
  const multiplier = Math.pow(10, precision || 0);
  return Math.round(value * multiplier) / multiplier;
}

export const getDate = (datetime) => datetime.split('T')[0];
export const metersToDistanceUnits = (meters, units) => round(meters * 0.000621371, 1);

export const secsToHMS = (secs) => {
  const sec_num = parseInt(secs, 10);
  const hours   = Math.floor(sec_num / 3600);
  const minutes = Math.floor(sec_num / 60) % 60;
  const seconds = sec_num % 60;

  return [hours,minutes,seconds]
    .map(v => v < 10 ? "0" + v : v)
    .filter((v,i) => v !== "00" || i > 0)
    .join(":")
};
