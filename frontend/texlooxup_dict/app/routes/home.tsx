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

{/*TODO: Implement pagination*/}
{/*TODO: Search in content and title*/}
{/*Default: Show all.*/}

export default function Home() {
  const [sectionsToSearchIn, setSectionsToSearchIn] = useState([]);
  const [resultSet, setResultSet] = useState(
    {
      excerptList: [],
      searchQuery: '',
    }
  );
  const [currentExcerpt, setCurrentExcerpt] = useState(
    {
      dir: null,
      file: null,
    }
  );
  const sectionList = {
    "concepts": "Concepts",
    "genops": "General Operations",
    "math": "Math",
    "miscellany": "Informational",
    "modes": "Modes",
    "pages": "Pages",
    "paras": "Paragraphs",
  };
  function populateSearchResultsByQuery(e) {
    const texSearchInput = document.getElementById("tex-search");
    if (texSearchInput.value === '') {
      alert("Please populate the search input box.");
    };
    const searchQuery = texSearchInput.value;
    const excerptList = getExcerptList()
      .filter(dirFile => {
        const [_, file] = dirFile;
        return file.startsWith(searchQuery);
      });
    setResultSet(
      {
        excerptList,
        searchQuery,
      }
    );
  };
  function populateSearchResultsByCategory(e) {
    const categoriesToInclude = [...document.querySelectorAll("input[name='tex-section']")]
      .filter(someInput => someInput.checked === true)
      .map(checkedInput => checkedInput.value);
    {/*for all checkbox input forms:
        check if checked
      if yes, add to running queue
      else ignore
        set filter by category*/}
    const excerptList = getExcerptList()
      .filter(dirFile => {
        const [dir, _] = dirFile;
        return categoriesToInclude.includes(dir);
      });
    setResultSet(
      {
        excerptList,
        searchQuery: "",
      }
    );
  };
  function changeExcerptSource(e) {
    const excerptPath = e.currentTarget.dataset.excerptpath;
    const impatientExcerptOutput = document.getElementById("impatient-excerpt");
    impatientExcerptOutput.src = "/entries/" + excerptPath;
  };
  return (
    <>
      <section>
        <h1>TeXLooXup</h1>
        <form action="">
        {/*TODO: Disable <Enter>-action*/}
          <input id="tex-search" type="search" required />
          <button onClick={populateSearchResultsByQuery} type="button">
            To be replaced by search-as-type
          </button>
          <fieldset>
            <legend>
              Sections to Search In
            </legend>
            {Object.entries(sectionList).map(nameTitle => {
              const [excerptDir, sectionTitle] = nameTitle;
              const name = "tex-section"
              return (
                <Fragment key={excerptDir}>
                  <label htmlFor={name}>{sectionTitle}</label>
                  <input
                    type="radio"
                    name={name}
                    onClick={populateSearchResultsByCategory}
                    value={excerptDir} />
                </Fragment>
              );
            })
            }
          </fieldset>
          <menu>
            {resultSet.excerptList.length > 0 ? resultSet.excerptList.map(filepath => {
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
                    {sectionTitle}: {excerptTitle}
                  </button>
                </li>
              );
            }) : resultSet.searchQuery !== '' && <p>No results found for '{resultSet.searchQuery}'.</p>}
          </menu>
        </form>
      </section>
      <iframe
        id="impatient-excerpt"
        width="1000px"
        height="900px"
        src={`/entries/${currentExcerpt.dir}/${currentExcerpt.file}`}>
        Instructions on how to use this thing go here.
      </iframe>
    </>
  );
}

