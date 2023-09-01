# VEOIBD Data Model

This is the repository hosting [VEOIBD data model](https://github.com/VEOIBD/data_models/blob/main/veoibd.data.model.csv) and a set of [standardized metadata terms](https://github.com/VEOIBD/data_models/tree/main/_data) that can be used to describe attributes in the data model. The data model defines attributes that are associated with a dataset type (e.g. clinical metadata) and their interdependencies. [Data Curator App (DCA)](https://dca.app.sagebionetworks.org/) pulls the data model when generating metadata template and validates manifests against it. This repository also houses the pipelines and workflows to streamline data model update and metadata dictonary management.  

# Updata Data Model and Metadata Dictionary
![data model update workflow](https://github.com/VEOIBD/data_models/assets/90745557/e061e265-77ff-4bca-a6bb-a525e79d3352)


**Step 1.** Pull most recent changes from the Main branch and create a new branch

**Step 2.** On the new branch, edit the veoibd.data.model.csv. The following columns are required to be filled: Attribute, Description, Required, Parent, Source. (See [Data Model Schema](https://sagebionetworks.jira.com/wiki/spaces/SCHEM/pages/2473623559/The+Data+Model+Schema) for details).If you'd like to clarify valid values of an attribute in the metadata dictionary, the **Module** and **Type** are required to be filled.  

**Step 3.** Push the changes to the remote branch and create a pull request (PR) to the Main branch. Creating a PR will trigger several GitHub Actions to: 
 1. Convert the veoibd.data.model.csv to jsonld file (i.e. veoibd.data.model.jsonld) that can be read by DCA and commit the changes to the PR via [ci-convert.yml](https://github.com/VEOIBD/data_models/blob/main/.github/workflows/ci-convert.yml)
 2. Add and update metadata term/template csv and markdown files that are used in the metadata dictionary static site and commit the changes to the PR via [update_metadata_dictionary.yml](https://github.com/VEOIBD/data_models/blob/main/.github/workflows/update_metadata_dictionary.yml)
 3. Build and publish the metadata dictionary site on GitHub pages via [pages.yml](https://github.com/VEOIBD/data_models/blob/main/.github/workflows/pages.yml)

# Update Metadata Dictionary Only

**Step 1.** Pull most recent changes from the Main branch and create a new branch

**Step 2.** On the new branch, edit terms csv files under \_data\ by adding Key Description and Source information.

**Step 3.** Push the changes to the remote branch and create a pull request (PR) to the Main branch. Creating a PR will trigger several GitHub Actions to: 
1. Add and update metadata template csv and markdown files that are used in the metadata dictionary static site and commit the changes to the PR via [update_metadata_dictionary.yml](https://github.com/VEOIBD/data_models/blob/main/.github/workflows/update_metadata_dictionary.yml)
2. Build and publish the metadata dictionary site on GitHub pages via [pages.yml](https://github.com/VEOIBD/data_models/blob/main/.github/workflows/pages.yml)

# VEOIBD Metadata Dictionary Site
VEOIBD Metadata Dictionary is a [Jekyll] site utilizing [Just the Docs] theme and is published on [GitHub Pages]. 

- `index.md` is the home page 
- `_config.yml` can be used to tweak Jekyll settings, such as theme, title
- `_data/` folder stores data for Jekyll to use when generating the site
- files in `docs/` will be accessed by GitHub Actions workflow to build the site

## Customization
You can add additional descriptions to home page or specific page by directly editing `index.md` or markdown files in `docs/`. 

## Building and previewing the site locally

1. Install Jekyll `gem install bundler jekyll`
2. Install Bundler `bundle install`
3. Run `bundle exec jekyll serve` to build your site and preview it at `http://localhost:4000`. The built site is stored in the directory `_site`.

## Publish site on GitHub pages
In addition to setting up the GitHub Actions workflow (i.e pages.yml), you need to allow deploying the GitHub pages using the workflow. Go to `Settings`-> `Pages` -> `Build and deployment`, then select `Source`: `GitHub Actions`.
