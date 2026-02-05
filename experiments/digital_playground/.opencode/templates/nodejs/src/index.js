// {{PROJECT_NAME}}
// Built with Guardian Framework

function main() {
  console.log("🚀 {{PROJECT_NAME}} is running");
  console.log("Use ./opencode-dual-agent.sh to start Guardian workflow");
}

if (require.main === module) {
  main();
}

module.exports = { main };
