# =============================================================================
# manifesto-pilot-data.R
# Loads, filters, and splits Manifesto Project data for pilot study
# =============================================================================

library(manifestoR)
library(dplyr)
library(tidyr)
library(stringr)

# --- 1. Authenticate --------------------------------------------------------
# The API key lives in code/R/manifesto_apikey.txt, which is gitignored.
# Copy manifesto_apikey.txt.example to manifesto_apikey.txt and paste your key.
mp_setapikey(key = readLines("manifesto_apikey.txt", warn = FALSE)[1])

# --- 2. Check available versions --------------------------------------------
mp_coreversions()
mp_corpusversions()

CORE_VERSION   <- "2025a"
CORPUS_VERSION <- "2025-1"

# Set the corpus version (separate from main dataset version)
mp_use_corpus_version(CORPUS_VERSION)

# --- 3. Download the main dataset -------------------------------------------
main_ds <- mp_maindataset(version = CORE_VERSION)

# Inspect column names so we know what we're working with
cat("\n=== Main dataset columns ===\n")
names(main_ds)
cat("\n=== Dimensions ===\n")
dim(main_ds)
head(main_ds)

# --- 4. Get the corpus (quasi-sentences + codes) ----------------------------
# mp_corpus() takes ids as a logical expression evaluated against mp_maindataset(),
# or a data.frame with party/date columns.
# We'll pull ALL available documents, then filter downstream.
# Use mp_corpus_df() which is shorthand for mp_corpus(..., as_tibble = TRUE).
cat("\n=== Downloading corpus (this may take a moment) ===\n")

corpus_df <- mp_corpus_df(
  TRUE,
  translation = "en",
  tibble_metadata = "all"
)

cat("\n=== Corpus columns ===\n")
names(corpus_df)
cat("\n=== Corpus dimensions ===\n")
dim(corpus_df)
head(corpus_df)

# --- 5. Map subcategory codes to main categories ----------------------------
# v5 codes look like "202_1", "103.2", "607_3" etc.
# We strip everything after the first 3 digits to get the parent main category.
# Special codes (000, 999, etc.) are excluded.

analysis_df <- corpus_df |>
  mutate(
    # Extract the 3-digit main category code from whatever format cmp_code is in
    main_code = str_extract(as.character(cmp_code), "^\\d{3}"),
    # Derive domain from first digit of main code
    domain = str_sub(main_code, 1, 1),
    domain_label = case_when(
      domain == "1" ~ "External Relations",
      domain == "2" ~ "Freedom and Democracy",
      domain == "3" ~ "Political System",
      domain == "4" ~ "Economy",
      domain == "5" ~ "Welfare and Quality of Life",
      domain == "6" ~ "Fabric of Society",
      domain == "7" ~ "Social Groups",
      TRUE          ~ NA_character_
    )
  ) |>
  # Drop uncoded (000), missing (999), and any codes that didn't match 3 digits
  filter(!is.na(main_code), !main_code %in% c("000", "999"))

cat("\n=== After filtering special codes ===\n")
cat("Total quasi-sentences:", nrow(analysis_df), "\n")
cat("Unique manifestos:", n_distinct(analysis_df$manifesto_id), "\n")
cat("Unique main categories:", n_distinct(analysis_df$main_code), "\n")

# --- 6. Inspect category distribution ---------------------------------------
cat("\n=== Quasi-sentences per main category ===\n")
analysis_df |>
  count(main_code, domain_label, sort = TRUE) |>
  print(n = 60)

# --- 7. Create 70/15/15 split at the manifesto level ------------------------
# Split by whole manifestos (not individual quasi-sentences) to avoid leakage
set.seed(42)

manifesto_ids <- unique(analysis_df$manifesto_id)
n <- length(manifesto_ids)

train_ids <- sample(manifesto_ids, size = floor(0.70 * n))
remaining <- setdiff(manifesto_ids, train_ids)
val_ids   <- sample(remaining, size = floor(0.50 * length(remaining)))
test_ids  <- setdiff(remaining, val_ids)

analysis_df <- analysis_df |>
  mutate(
    split = case_when(
      manifesto_id %in% train_ids ~ "train",
      manifesto_id %in% val_ids   ~ "val",
      manifesto_id %in% test_ids  ~ "test"
    )
  )

cat("\n=== Split summary ===\n")
analysis_df |>
  group_by(split) |>
  summarise(
    n_quasi_sentences = n(),
    n_manifestos = n_distinct(manifesto_id),
    n_categories = n_distinct(main_code)
  ) |>
  print()

# --- 8. Save ----------------------------------------------------------------
dir.create("data", showWarnings = FALSE, recursive = TRUE)

saveRDS(analysis_df, file = "data/manifesto-pilot-dataset.rds")
write.csv(analysis_df, file = "data/manifesto-pilot-dataset.csv", row.names = FALSE)

cat("\n=== Saved to data/manifesto-pilot-dataset.rds and .csv ===\n")
