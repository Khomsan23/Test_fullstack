module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    "plugin:vue/vue3-recommended", // เปลี่ยนเป็น vue3-recommended หากคุณใช้ Vue 3
    "eslint:recommended",
    "plugin:prettier/recommended",
  ],
  parserOptions: {
    parser: "@babel/eslint-parser",
    requireConfigFile: false, // เพิ่มตัวเลือกนี้เพื่อหลีกเลี่ยงปัญหากับ Babel config
  },
  rules: {
    "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "warn" : "off",
    "prettier/prettier": [
      "error",
      {
        endOfLine: "auto", // แก้ปัญหา line endings
      },
    ],
  },
};
