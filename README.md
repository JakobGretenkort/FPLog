# FPLog
FPLog is a system to check if websites are using browser fingerprinting and to log exactly the fingerprinting related access patterns the website exhibits.

# Setup
## Download Firefox
Because this tool relies on building a custom firefox, you will need to be able to build firefox.

Follow this tutorial: https://firefox-source-docs.mozilla.org/setup/linux_build.html#building-firefox-on-linux and use the `--vsc=git` option for `bootstrap.py`.

## Apply Patch
The patch file provided in the browser directory is based on a particular version of the firefox repo.
To create a new branch in your repo which is rolled back to that version, use `git checkout -b fplog afe4a81b75570060a6fff08e88bca33a34636b60`.

Now you can apply the patch file from this repo. Copy it into your firefox repo and run `git apply browser_mod.patch`.

## Build Firefox
First, you may want to go to the file fplog/fplog.cpp and adjust the constant 'LOG_PATH' to the path where you want to store the logfiles FPLog will generate.

Now, build firefox by running the following command in its root directory: `./mach build`.

This will take a while. Once completed, you can run the custom firefox with the command `./mach run`.

## Configure Firefox
Run your firefox and go to `about:config` and set `security.sandbox.content.level` to `1`.

## Build the Extension
Go to the extension folder and run `python3 build.py`.

You can add the extension to the newly built firefox in the `about:debugging` tab.

## Selenium
If you want to have FPLog visit websites automatically, you will need to install Selenium (www.selenium.dev).

# Usage
At this point, you can simply visit a site with FPLog to generate logfiles which show what javascript APIs the visited site makes access to. The logfiles can be found at the location configured in the 'Build Firefox' step.

If you want to have a list of websites visited automatically, you may put a csv with the columns index (int) and url in the automation folder, adjust the path of the BINARY constant in the script 'selenium_script.py' and run that script with `python3 selenium_script.py`. 

