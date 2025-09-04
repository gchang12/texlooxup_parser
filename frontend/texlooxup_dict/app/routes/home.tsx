import {
  useState,
  Fragment,
} from 'react';
import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

import {
  getExcerptList,
} from '../staticData/excerptList.ts';

export function meta({}: Route.MetaArgs) {
  return [
    { title: "TexLooXup - TeX-command search utility" },
    { name: "description", content: "For looking up TeX command definitions" },
  ];
}

export default function Home() {
  const sectionList = {
    "concepts": "Concepts",
    "genops": "General Operations",
    "math": "Math",
    "miscellany": "Informational",
    "modes": "Modes",
    "pages": "Pages",
    "paras": "Paragraphs",
  };
  const [searchParams, setSearchParams] = useState(
    {
      categories: Object.keys(sectionList),
      queryStr: '',
    }
  );
  const [currentExcerpt, setCurrentExcerpt] = useState(
    {
      dir: "_internal",
      file: "how-to-use.html",
    }
  );
  {/*const [showCategories, setShowCategories] = useState(false);*/}
  function getCategoriesToInclude() {
    const categoriesToInclude = [...document.querySelectorAll("input[name='tex-section']")]
      .filter(someInput => someInput.checked === true)
      .map(checkedInput => checkedInput.value);
    return categoriesToInclude;
  };
  function populateSearchResultsByQuery(e) {
    const texSearchInput = document.getElementById("tex-search");
    const queryStr = texSearchInput.value;
    setSearchParams(
      {
        ...searchParams,
        queryStr,
      }
    );
  };
  function populateSearchResultsByCategory(e) {
    const categories = getCategoriesToInclude();
    setSearchParams(
      {
        ...searchParams,
        categories,
      }
    );
  };
  function changeExcerptSource(e) {
    const excerptPath = e.currentTarget.dataset.excerptpath;
    const impatientExcerptOutput = document.getElementById("impatient-excerpt");
    impatientExcerptOutput.src = "/entries/" + excerptPath;
  };
  function searchForCommand(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      populateSearchResultsByQuery(e);
    };
  };
  const excerptList = getExcerptList()
    .filter(filepath => {
      const [excerptDir, excerptFile] = filepath;
      return (
        searchParams.categories.includes(excerptDir) && excerptFile.toLowerCase().includes(searchParams.queryStr.toLowerCase())
      );
    });
  return (
    <>
      <section>
        <h1>TeXLooXup</h1>
        <form action="">
        {/*TODO: Disable <Enter>-action*/}
          {/*<button onClick={populateSearchResultsByQuery} type="button"> To be replaced by search-as-type </button>*/}
          <fieldset>
            <legend>
              Search in Categories:
            </legend>
            {/*<div className="category-list-toggle"> <label htmlFor="show-categories">Show</label> <input type="checkbox" name="show-categories" onClick={e => setShowCategories(e.currentTarget.checked)} /> </div>*/}
            <div className="category-list">
            {Object.entries(sectionList).map(nameTitle => {
              const [excerptDir, sectionTitle] = nameTitle;
              const name = "tex-section"
              return (
                <div className="category-toggle" key={excerptDir}>
                  <label htmlFor={name}>{sectionTitle}</label>
                  <input
                    type="checkbox"
                    name={name}
                    onChange={populateSearchResultsByCategory}
                    defaultChecked={true}
                    value={excerptDir} />
                </div>
              );
            })
            }
            </div>
          </fieldset>
          <div className="searchbar">
            <label htmlFor="tex-search">Command Search</label>
            <input spellcheck={false} name="tex-search" onKeyDown={searchForCommand} id="tex-search" type="search" required />
          </div>
          <menu>
            {excerptList.length > 0 ? excerptList.map(filepath => {
              const [excerptDir, excerptFile] = filepath;
              const sectionTitle = sectionList[excerptDir];
              let excerptTitle;
              if (["miscellany", "concepts"].includes(excerptDir)) {
                excerptTitle = excerptFile.replace('.pdf', '');
              } else {
                const excerptName = (excerptFile.startsWith("_") ? excerptFile.slice(1) : "\\" + excerptFile).replace('.pdf', '');
                excerptTitle = excerptName.startsWith("\\") ? <code>{excerptName}</code> : excerptName;
              };
              return (
                <li key={`${excerptDir}/${excerptFile}`}>
                  <button
                    type="button"
                    className={sectionTitle}
                    data-excerptpath={`${excerptDir}/${excerptFile}`}
                    onClick={changeExcerptSource}>
                    <span className="excerpt-dir">{sectionTitle}</span>
                    <span className="excerpt-file">{excerptTitle}</span>
                  </button>
                </li>
              );
            }) : <p id="empty-resultset-notification">No results found for '{searchParams.queryStr}'.</p>}
          </menu>
        </form>
      </section>
      <iframe
        id="impatient-excerpt"
        width="1000px"
        height="800px"
        src={`/entries/${currentExcerpt.dir}/${currentExcerpt.file}`}>
        Instructions on how to use this thing go here.
      </iframe>
    </>
  );
}



