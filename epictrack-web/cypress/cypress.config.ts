import { defineConfig } from "cypress";

export default defineConfig({
  supportFolder: "support",
  component: {
    supportFile: "support/component.tsx",
    devServer: {
      framework: "create-react-app",
      bundler: "webpack",
    },
  },
});
