import axios from "axios";
const NODE_ENV = import.meta.env.VITE_NODE_ENV;
const VUE_APP_CLIENT_ID = import.meta.env.VITE_VUE_APP_CLIENT_ID;
const URL_LOCAL = `http://${location.host}`;
const URL_LIVE = "https://medalcase.com";

const STREAKS_LOCAL = "http://localhost:5180";
const STREAKS_LIVE = "https://medalcase.com/v1/";
export const SCOPES = [
  "read",
  "profile:read_all",
  "activity:read",
  "activity:read_all"
];
const redirectUrl = NODE_ENV === "production" ? URL_LIVE : URL_LOCAL;
const streaksAPI = NODE_ENV === "production" ? STREAKS_LIVE : STREAKS_LOCAL;
export const URL = {
  login: `${streaksAPI}/athlete/login`,
  list: `${streaksAPI}/athlete`,
};
export const STRAVA_OAUTH_URL = `https://www.strava.com/oauth/authorize?client_id=${VUE_APP_CLIENT_ID}&response_type=code&redirect_uri=${redirectUrl}/exchange_token&approval_prompt=force&scope=${SCOPES.join(
  ","
)}`;


export const authHeader = () => {
  let token = getJWT();
  if (token) {
    return { Authorization: `Bearer ${token}` };
  } else {
    return {};
  }
};

