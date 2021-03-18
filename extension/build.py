import os;

def main():
  buildInjector();

def buildInjector():
  script_dir = os.path.dirname(__file__);
  logger_path = os.path.join(script_dir, "src/logger.js");
  injector_path = os.path.join(script_dir, "build/injector.js");

  with open(logger_path, "r") as logger, open(injector_path, "w") as injector:
    injector.write("function inject() {\n");
    injector.write("  window.eval(`\n");

    line = logger.readline();
    while line != '':
      injector.write(line.replace('\\', '\\\\'));
      line = logger.readline();

    injector.write("  `);\n");
    injector.write("}\n");
    injector.write("\n");
    injector.write("inject();\n");

if __name__ == "__main__":
    main()