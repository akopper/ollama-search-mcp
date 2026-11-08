---
name: Ollama Web Search
description: Web search and page fetching via the ollama-search MCP (web_search/web_fetch) – for current information, research, documentation, and source verification.
---

# Ollama Web Search

The `ollama-search` MCP server exposes two tools: **web_search** and
**web_fetch**.

## web_search

| Parameter     | Required | Description                                    |
| ------------- | -------- | ---------------------------------------------- |
| `query`       | yes      | Search query                                   |
| `max_results` | no       | Number of results, default `10`, maximum `10`  |

Returns:

```json
{
  "results": [
    { "title": "…", "url": "https://…", "content": "…" }
  ]
}
```

## web_fetch

| Parameter | Required | Description                            |
| --------- | -------- | -------------------------------------- |
| `url`     | yes      | Absolute URL, including `https://`     |

Returns an object with `title`, `content`, and `links`.

## Calling from Code Mode

```js
const result = await tools["ollama-search"].web_search({
  query: "ollama web search api",
  max_results: 5,
});
return result;
```

```js
const page = await tools["ollama-search"].web_fetch({
  url: "https://opencode.ai/docs/skills",
});
return page;
```

Independent calls in parallel:

```js
const [search, page] = await Promise.allSettled([
  tools["ollama-search"].web_search({ query: "…", max_results: 5 }),
  tools["ollama-search"].web_fetch({ url: "https://…" }),
]);
```

Outside Code Mode the tools are named `web_search` and `web_fetch`, possibly
with a server prefix – use the names from the session's tool list.

## Pitfalls

- `content` can be very long: keep only the relevant excerpts.
- Search queries and URLs are sent to Ollama's cloud service – never send
  confidential data.
- No results: rephrase the query or try English terms.
- `web_fetch` fails: check the absolute or canonical URL, otherwise use the
  search snippet.
- The server does not show up in the tool list and the log says
  `mcp connect failed … NotFound: ChildProcess.spawn (uvx …)`: the `PATH` of
  the OpenCode process lacks `~/.local/bin`. Desktop launches skip `~/.bashrc`,
  so use the absolute path to `uvx` in the MCP config.
- `web_search` returns `Error executing tool web_search` and the log says
  `Authorization header with Bearer token is required for web search`:
  `OLLAMA_API_KEY` was empty. Set it literally in the MCP config, or export it
  in the environment that launches OpenCode.
