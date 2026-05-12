load_votes <- function() {
  vt <- read_csv("../data/votes.csv") |>
    janitor::clean_names() |>
    rename(
      participant = voter_id
    ) |>
    mutate(
      datetime = datetime |>
        parse_date_time(orders = "a b d Y H:M:S z")
    )

  return(vt)
}

load_themes <- function() {
  themes <- read_csv("../data/themes.csv")

  return(themes)
}

parse_yes_no <- function(x) {
  case_when(
    x == "yes" ~ TRUE,
    x == "no" ~ FALSE,
    .default = NA
  )
}

load_comments <- function(
  label_columns = c(
    "is_actionable"
  )
) {
  # Load votes to calculate vote counts
  vt <- load_votes()

  vote_counts <- vt |>
    group_by(comment_id) |>
    summarise(
      agrees = sum(vote == 1, na.rm = TRUE),
      disagrees = sum(vote == -1, na.rm = TRUE),
      neutrals = sum(vote == 0, na.rm = TRUE),
      total_votes = n(),
      .groups = "drop"
    )

  # Download latest version from:
  # https://docs.google.com/spreadsheets/d/1CGdvpwiBB6PJXdEbRKLdgWhW1eU0i-FVhoJ7QuYSqzY/gviz/tq?tqx=out:csv&sheet=Sheet1
  comments_labels <- read_csv("../data/comments_labels.csv") |>
    janitor::clean_names() |>
    select(comment_id, all_of(label_columns)) |>
    mutate(
      is_actionable = parse_yes_no(is_actionable)
    )

  cm <- read_csv("../data/comments.csv") |>
    janitor::clean_names() |>
    left_join(comments_labels, by = "comment_id") |>
    mutate(
      datetime = datetime |>
        parse_date_time(orders = "a b d Y H:M:S z"),

      comment_body = comment_body |>
        # Special string characters
        str_replace_all("“", "\"") |>
        str_replace_all("”", "\"") |>
        # FAccT misspellings
        str_replace_all(fixed("faact", ignore_case = TRUE), "FAccT") |>
        # Consistent capitalization
        str_replace_all(fixed("facct", ignore_case = TRUE), "FAccT"),

      statement_type = case_when(
        str_detect(comment_body, "^(?i)facct is doing well in") ~ "facct is doing well in",
        str_detect(comment_body, "^(?i)facct is not doing well in") ~ "facct is not doing well in",
        str_detect(comment_body, "^(?i)facct should not") ~ "facct should not",
        str_detect(comment_body, "^(?i)facct should") ~ "facct should",
        str_detect(comment_body, "^(?i)facct is not") ~ "facct is not",
        str_detect(comment_body, "^(?i)facct is") ~ "facct is",
        .default = "other"
      ) |>
        factor(levels = c(
          "facct is doing well in",
          "facct is not doing well in",
          "facct should",
          "facct should not",
          "facct is",
          "facct is not",
          "other"
        ))
    ) |>
    mutate(
      comment_day = date(datetime)
    ) |>
    rename(
      cm_agrees = agrees,
      cm_disagrees = disagrees
    ) %>%
    left_join(vote_counts, by = "comment_id") |>
    mutate(
      agree_pct = (agrees / total_votes) * 100,
      disagree_pct = (disagrees / total_votes) * 100,
      neutral_pct = (neutrals / total_votes) * 100
    ) %>%
    rowwise() %>%
    mutate(
      consensus_num = max(agree_pct, disagree_pct, neutral_pct) - min(agree_pct, disagree_pct, neutral_pct),
      consensus_inv = -consensus_num
    ) %>%
    ungroup()

  return(cm)
}

load_participants <- function() {
  pt_raw <- read_csv("../data/participant-votes.csv") |>
    janitor::clean_names() |>
    mutate(
      group_id = as.factor(group_id)
    )

  return(pt_raw)
}
