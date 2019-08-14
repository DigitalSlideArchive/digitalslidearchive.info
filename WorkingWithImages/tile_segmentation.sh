docker run \
     -it --rm -p3334:8888 \
     -v "${PWD}:/app:rw" \
     -v "${PWD}:/data/code:rw" \
     -v "/HCP_Data/TCGAResults/results:/data/output/results:rw" \
     -v "/HCP_Data/TCGAResults/histo_tile_50k_data/train:/data/train:rw" \
     -v "/HCP_Data/TCGAResults/histo_tile_50k_data/test:/data/test:rw" \
     fgiuste/histomicstk
