# TODO

This file tracks future work, improvements, and testing tasks for AudioMeta Python.

## Rating Profile Compatibility Testing

### High Priority

- [ ] **Test rating profile compatibility across different audio players**
  - Verify which rating values are actually readable and display correctly
  - Test Profile A (255 non-proportional) with Windows Media Player, MusicBee, Winamp, kid3
  - Test Profile B (100 proportional) with FLAC players and Vorbis-compatible software
  - Test Profile C (255 proportional) with Traktor Pro and Traktor DJ

## Feature Enhancements

### Medium Priority

- [ ] **OGG file support**

  - Currently planned but not implemented
  - Vorbis comment support for OGG files
  - Integration with existing Vorbis manager

- [ ] **Batch processing with parallelization**
  - Add support for processing multiple audio files simultaneously
  - Implement parallel metadata reading/writing operations
  - Add progress tracking and error handling for batch operations
  - Consider thread pool or multiprocessing for CPU-intensive tasks

---

## Contributing

If you'd like to work on any of these items:

1. Check if there's already an open issue for the task
2. Create a new issue if needed
3. Fork the repository and create a feature branch
4. Implement your changes with appropriate tests
5. Submit a pull request

For questions about specific tasks, please open an issue for discussion.
