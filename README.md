# FPLog
FPLog is a system to check if websites are using browser fingerprinting and to log exactly the fingerprinting related access patterns the website exhibits.

# Setup
## Download Firefox
Because this tool relies on building a custom firefox, you will need to be able to build firefox.

Follow this tutorial: https://firefox-source-docs.mozilla.org/setup/linux_build.html#building-firefox-on-linux and use the `--vsc=git` option for `bootstrap.py`.

## Apply Patch
The patch file provided in the browser directory is based on a particular version of the firefox repo.
To create a new branch in your repo which is rolled back to that version, use `git checkout -b fplog afe4a81b755`.

Now you can apply the patch file from this repo. Copy it into your firefox repo and run `git apply browser_mod.patch`.

## Build Firefox
Now, build firefox by running the following command in its root directory: `./mach build`.

This will take a while. Once completed, you can run the custom firefox with the command `./mach run`.

## Configure Firefox
Run your firefox and go to `about:config` and set `security.sandbox.content.level` to `1`.

## Build the Extension
Go to the extension folder and run `python3 build.py`.

# Usage
TODO...

