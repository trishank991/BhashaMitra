# Seed Vocabulary Images Command

This Django management command adds image URLs to vocabulary words using free image APIs.

## Usage

```bash
python manage.py seed_vocabulary_images [OPTIONS]
```

## Options

- `--language LANGUAGE` - Language to update (default: HINDI)
- `--dry-run` - Show what would be updated without making changes
- `--theme THEME` - Only update words from specific theme (e.g., Animals, Colors, Family)
- `--source {unsplash,picsum,picsum-seed}` - Image source API to use (default: unsplash)
- `--overwrite` - Overwrite existing image URLs
- `--validate` - Validate that URLs return valid images (requires requests library)

## Image Sources

### Unsplash Source API (Default)
- URL format: `https://source.unsplash.com/400x300/?{keywords}`
- Uses English translation + theme-specific keywords
- Best quality images
- Examples:
  - Dog: `https://source.unsplash.com/400x300/?dog,animal,wildlife,pet`
  - Red: `https://source.unsplash.com/400x300/?red,colorful,paint,abstract`

### Picsum Photos
- URL format: `https://picsum.photos/400/300`
- Random images
- No keyword matching

### Picsum Photos with Seed
- URL format: `https://picsum.photos/seed/{word_id}/400/300`
- Consistent images based on word ID
- No keyword matching

## Category-Specific Keywords

The command automatically adds theme-specific keywords to improve image relevance:

- **Family**: family, people, portrait
- **Colors**: colorful, paint, abstract
- **Numbers**: numbers, counting, math
- **Animals**: animal, wildlife, pet
- **Food**: food, fruit, vegetable, meal
- **Body Parts**: human, body, anatomy
- **Greetings**: hello, wave, greeting, smile
- **Actions**: action, motion, activity

## Examples

### Basic usage - Add images to all Hindi words without images
```bash
python manage.py seed_vocabulary_images --language=HINDI
```

### Dry run to preview changes
```bash
python manage.py seed_vocabulary_images --language=HINDI --dry-run
```

### Update only Animals theme
```bash
python manage.py seed_vocabulary_images --language=HINDI --theme=Animals
```

### Update using Picsum with seed for consistent images
```bash
python manage.py seed_vocabulary_images --language=HINDI --source=picsum-seed
```

### Overwrite existing images with new Unsplash URLs
```bash
python manage.py seed_vocabulary_images --language=HINDI --overwrite
```

### Validate URLs (requires requests library)
```bash
python manage.py seed_vocabulary_images --language=HINDI --validate
```

## Output

The command provides detailed progress output:
- Shows each word being processed with its theme and keywords
- Displays final statistics (total processed, updated, failed)
- Color-coded output (success = green, error = red, warning = yellow)

## Notes

- By default, the command only updates words that don't have an image URL
- Use `--overwrite` to update all words regardless of existing images
- Unsplash Source API provides the best image quality and relevance
- URLs are stored in the `image_url` field of VocabularyWord model
- No API key required for any of the free image sources
- Images are served dynamically, no storage required
