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
      categories: [],
      queryStr: '',
    }
  );
  function suppressSubmit(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      populateSearchResults(e);
    };
  };
  function prettifyExcerptTitle({excerptDir, excerptFile}) {
    const sectionTitle = sectionList[excerptDir];
    let excerptTitle;
    if (["miscellany", "concepts"].includes(excerptDir)) {
      excerptTitle = excerptFile.replace('.pdf', '');
    } else {
      const excerptName = (excerptFile.startsWith("_") ? excerptFile.slice(1) : "\\" + excerptFile).replace('.pdf', '');
      {/* excerptTitle = excerptName.startsWith("\\") ? <code>{excerptName}</code> : excerptName; */}
      excerptTitle = excerptName;
    };
    return [sectionTitle, excerptTitle];
  };
  function populateSearchResults(e) {
    const texSearchInput = document.getElementById("tex-search");
    const queryStr = texSearchInput.value;
    const categories = [...document.querySelectorAll("input[name='tex-section']")]
      .filter(someInput => someInput.checked === true)
      .map(checkedInput => checkedInput.value);
    setSearchParams(
      {
        categories,
        queryStr,
      }
    );
  };
  function changeExcerptSource(e) {
    const excerptButton = e.currentTarget;
    // Change source
    const excerptPath = excerptButton.dataset.excerptpath;
    const impatientExcerpt = document.getElementById("impatient-excerpt");
    const excerptIframe = impatientExcerpt.querySelector("iframe");
    excerptIframe.src = "/entries/" + excerptPath;
    // Set h1 and h2
    const [excerptDir, excerptFile] = excerptPath.split('/');
    const [sectionTitle, excerptTitle] = prettifyExcerptTitle({excerptDir, excerptFile});
    impatientExcerpt.querySelector("h1").textContent = sectionTitle;
    impatientExcerpt.querySelector("h2").textContent = excerptTitle;
    // add class.
    const activeExcerptLabel = "active-excerpt";
    document.querySelectorAll("." + activeExcerptLabel).forEach(node => node.classList.remove(activeExcerptLabel));
    excerptButton.classList.add(activeExcerptLabel);
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
                    defaultChecked={false}
                    value={excerptDir} />
                </div>
              );
            })
            }
            </div>
          </fieldset>
          <div className="searchbar">
            <label htmlFor="tex-search">Command Search</label>
            <input spellCheck={false} name="tex-search" onKeyDown={suppressSubmit} id="tex-search" type="search" required />
          </div>
          <button type="button" onClick={populateSearchResults}>Search!</button>
        </form>
        <form>
          <menu>
            {excerptList.length > 0 ? excerptList.map(filepath => {
              const [excerptDir, excerptFile] = filepath;
              const [sectionTitle, excerptTitle] = prettifyExcerptTitle({excerptDir, excerptFile});
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
      <section id="impatient-excerpt">
        <h1></h1>
        <h2></h2>
        <iframe
          width="1000px"
          height="800px"
          src={`/entries/_internal/how-to-use.html`}>
        </iframe>
      </section>
    </>
  );
}



