# Static Site Generator

Static Site Generator based on "Build a Static Site Generator" course from Boot.dev

---

## Usage:

Build the structure and html files with `./build.sh`. Basepath can be specified with the flag `basepath`, otherwise defaults to "/"
Content stored in the `content` folder will be used, along with the template sitting in the root directory. Files will be built and copied to `docs`

### Notes:

Works best with clearly formatted Markdown files. Files must start with a "h1" heading, i.e. `#`
