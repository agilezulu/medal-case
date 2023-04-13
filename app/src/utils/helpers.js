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

export const slugify = (text) => {
  return text
    .toString()                           // Cast to string (optional)
    .normalize('NFKD')            // The normalize() using NFKD method returns the Unicode Normalization Form of a given string.
    .toLowerCase()                  // Convert the string to lowercase letters
    .trim()                                  // Remove whitespace from both sides of a string (optional)
    .replace(/\s+/g, '-')            // Replace spaces with -
    .replace(/[^\w-]+/g, '')     // Remove all non-word chars
    .replace(/--+/g, '-');        // Replace multiple - with single -
};

const compare = (key) => ( a, b ) => {
  if ( a[key] < b[key] ){
    return -1;
  }
  if ( a[key] > b[key] ){
    return 1;
  }
  return 0;
};

export const groupBy = (data, groupKey, keys, gsortKey) => {
  return data.reduce(function (storage, item) {
    var group = item[groupKey];
    if (keys) {
      // if passed additional keys -> define group attributes
      let keyMap = keys.map((k) => [k, item[k]]);
      let grp = Object.fromEntries(keyMap);
      grp.gKey = group;
      grp.gVal = [];
      grp.gCount = 0;
      grp.gRaceCount = 0

      storage[group] = storage[group] || grp;
      storage[group].gVal.push(item);
      if (gsortKey) {
        storage[group].gVal.sort(compare(gsortKey));
      }
      if (groupKey === 'class_key' && item.race) {
        storage[group].gRaceCount++;
      }
      storage[group].gCount++;


    } else {
      // simple grouping using group name as key
      storage[group] = storage[group] || [];
      storage[group].push(item);
      if (gsortKey) {
        storage[group].sort(compare(gsortKey));
      }
    }
    return storage;
  }, {});
};
