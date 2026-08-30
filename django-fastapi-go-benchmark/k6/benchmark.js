import http from 'k6/http';
import { check } from 'k6';

const TARGETS = {
  django: 'http://django:8000',
  fastapi: 'http://fastapi:8000',
  'fastapi-granian': 'http://fastapi-granian:8000',
  golang: 'http://golang:8000',
};

export const options = {
    vus: Number(__ENV.VUS || 30),
    duration: __ENV.DURATION || '30s',

    summaryTrendStats: [
        "min",
        "med",
        "avg",
        "max",
        "p(90)",
        "p(95)",
        "p(99)",
    ],

    thresholds: {
        http_req_failed: ["rate<0.01"],
    },
};

export default function () {
  const target = TARGETS[__ENV.TARGET || 'django'];
  // const res = http.get(`${target}/users/${__ENV.USER_ID || 5000}`);
  // check(res, { 'status 200': r => r.status === 200 });

  const res = http.get(
    `${target}/users/${__ENV.USER_ID || 5000}`,
    {
        timeout: '10s',
    }
  );

  if (res.status !== 200) {
      console.log(
          `FAILED: status=${res.status} error=${res.error} error_code=${res.error_code}`
      );
  }

  check(res, {
      'status is 200': r => r.status === 200,
  });
}

export function handleSummary(data) {
  const vus=__ENV.VUS || '1'
  const target = __ENV.TARGET || 'django';
  return { [`/results/${target}_${vus}vus.json`]: JSON.stringify(data) };
}
