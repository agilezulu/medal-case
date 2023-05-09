import moment from "moment";

export const jwtKey = "medalcase_jwt";
export const userKey = "medalcase_user";
export const setJWT = (token) => window.localStorage.setItem(jwtKey, token);
export const getJWT = () => window.localStorage.getItem(jwtKey);
export const removeJWT = () => window.localStorage.removeItem(jwtKey);
export const setUser = (data) => window.localStorage.setItem(userKey, JSON.stringify(data));
export const getUser = () => JSON.parse(window.localStorage.getItem(userKey));
export const removeUSER = () => window.localStorage.removeItem(userKey);

export const formatDate = (dateStr, formatStr) => {
  let format = formatStr || 'ddd Do MMMM YYYY';
  return moment(dateStr).format(format);
}
export const round = (value, precision) => {
  const multiplier = Math.pow(10, precision || 0);
  return Math.round(value * multiplier) / multiplier;
}

export const getDate = (datetime) => datetime.split('T')[0];
export const metersToDistanceUnits = (meters, selectedUnits) => {
  if (!meters) { return 0; }
  return round(meters * (selectedUnits === 'km' ? 0.001 : 0.000621371), 1) + ` ${selectedUnits}`;
}
export const metersToDistanceValue = (meters, selectedUnits) => {
  if (!meters) { return 0; }
  return round(meters * (selectedUnits === 'km' ? 0.001 : 0.000621371), 1);
}

export const metersFromDistanceUnits = (distance, units) => {
  if (units === 'mi'){
    return distance * 1609.34;
  }
  else if (units === 'km'){
    return distance * 1000;
  }
  else {
    console.error("Invalid units for conversion");
  }
}

export const miToKm = (miles) => {
  if (!miles) { return 0; }
  return round(miles * 1.60934, 1);
}
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

const compare = (key, dir) => ( a, b ) => {
  const usedir = dir || 'asc';
  if (usedir === 'asc') {
    if (a[key] < b[key]) {
      return -1;
    }
    if (a[key] > b[key]) {
      return 1;
    }
  }
  else {
    if ( a[key] > b[key] ){
      return -1;
    }
    if ( a[key] < b[key] ){
      return 1;
    }
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
      grp.pb = 999999999999;

      storage[group] = storage[group] || grp;
      storage[group].gVal.push(item);
      if (gsortKey) {
        storage[group].gVal.sort(compare(gsortKey, 'desc'));
      }
      // store pb
      if (parseInt(item.elapsed_time, 10) < storage[group].pb){
        storage[group].pb = item.elapsed_time;
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
