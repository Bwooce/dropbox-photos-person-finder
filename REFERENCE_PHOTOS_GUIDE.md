# Reference Photos Guide

## How Many Photos Do You Need?

### Minimum: 2-3 photos
- Basic recognition, but may miss some matches
- Use this if you have limited good photos

### Recommended: 3-5 photos
- **Sweet spot for most use cases**
- Good balance of accuracy and processing speed
- Covers most variations in appearance

### Maximum: 5-8 photos
- Best accuracy for challenging cases
- Use when the person appears very differently across photos
- Diminishing returns beyond 8 photos

## What Kind of Photos Work Best?

### ✅ EXCELLENT Reference Photos

1. **High Resolution**
   - Minimum 300x300 pixels for the face area
   - Prefer 500x500 or larger
   - Clear, sharp focus

2. **Good Lighting**
   - Natural daylight is best
   - Even lighting across the face
   - Avoid harsh shadows

3. **Direct Face View**
   - Face looking toward camera
   - Front-facing or slight angle (up to 30 degrees)
   - Face takes up at least 20% of image

4. **Clear Features**
   - Eyes, nose, mouth clearly visible
   - No sunglasses or masks
   - Minimal hair covering face

### ⚠️ ACCEPTABLE Reference Photos

1. **Slight Angles**
   - Profile shots (side view) can work
   - 3/4 view angles
   - Slight head tilt

2. **Different Expressions**
   - Smiling vs neutral
   - Different emotions
   - Helps with expression variations

3. **Different Ages/Times**
   - Recent photos preferred
   - But older photos can help with age variations
   - Mix of different time periods if available

### ❌ AVOID These Reference Photos

1. **Poor Quality**
   - Blurry or out of focus
   - Very low resolution
   - Over/under exposed

2. **Obscured Face**
   - Sunglasses or masks
   - Hair covering significant portions
   - Hand partially blocking face

3. **Extreme Angles**
   - Looking completely away
   - Extreme up/down angles
   - Back of head only

4. **Group Photos**
   - Face too small in frame
   - Multiple people confusing the algorithm
   - Poor crop of individual

## Ideal Reference Photo Set

### Example 5-Photo Set:
1. **Straight-on headshot** (passport style)
2. **Smiling casual photo** (natural lighting)
3. **Slight angle view** (3/4 profile)
4. **Different lighting** (indoor vs outdoor)
5. **Recent full-face photo** (clear and sharp)

### Diversity Helps:
- **Lighting conditions**: Indoor, outdoor, artificial light
- **Expressions**: Neutral, smiling, serious
- **Angles**: Front-facing, slight angles
- **Time periods**: Recent and older (if appearance changed)
- **Settings**: Formal and casual photos

## Pro Tips

### 📸 Cropping Reference Photos
- Crop to include head and shoulders
- Don't crop too tight - include some context
- Square aspect ratio works well
- Keep original proportions when possible

### 🔧 Technical Settings
- Save as JPG or PNG
- Avoid over-compression
- Keep file sizes reasonable (100KB - 2MB each)
- Consistent naming (person1.jpg, person2.jpg, etc.)

### 🎯 Quality Check
Before processing, verify each reference photo:
- [ ] Face clearly visible
- [ ] Good lighting
- [ ] Sharp focus
- [ ] Appropriate size
- [ ] No obstructions

## Common Mistakes to Avoid

1. **Using only one photo** - Not enough data for accurate matching
2. **All photos too similar** - Same angle, lighting, expression
3. **Photos too old** - If appearance has changed significantly
4. **Low quality screenshots** - From social media, video calls
5. **Heavy filters/editing** - Can confuse the recognition algorithm

## Testing Your Reference Photos

Run the `test_references.py` script (if created) to verify:
- All reference photos contain detectable faces
- Quality is sufficient for encoding
- Set provides good diversity

## Face Recognition Accuracy by Photo Quality

| Photo Quality | Expected Accuracy |
|---------------|-------------------|
| Excellent (5+ good photos) | 85-95% |
| Good (3-4 decent photos) | 75-85% |
| Fair (2-3 average photos) | 60-75% |
| Poor (1-2 bad photos) | 30-60% |

Remember: Better reference photos = better results finding matching photos in your Dropbox folder!